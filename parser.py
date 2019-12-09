import numpy as np
import ephem

def parseSatellite(filenameTLE, filenameSavedPass):

	tleFile = open(filenameTLE, "r")
	sat = ephem.readtle(
		tleFile.readline(),
		tleFile.readline(),
		tleFile.readline()
	)
	tleFile.close()

	loc = ephem.Observer()
	savedPassFile = open(filenameSavedPass, "r")
	loc.lat = float(savedPassFile.readline()) * ephem.degree
	loc.lon = float(savedPassFile.readline()) * ephem.degree
	loc.elevation = float(savedPassFile.readline()) 

	startTime = ephem.Date(savedPassFile.readline()) + ephem.second * 75
	savedPassFile.close()

	return sat, loc, startTime

def write(tau_res, outfile, events_array):

	# divide by timestamp resolution
	timestamps_array = np.asarray([event[0] for event in events_array]) / tau_res
	# print(timestamps_array[0:100])

	# 2 ^ detector_index
	patterns_array = 2 ** np.asarray([event[1] for event in events_array]) 
	# print(patterns_array[0:100])

	# shift bits and force types
	timestamps_array = timestamps_array.astype('uint64') << 15
	patterns_array = patterns_array.astype('uint64')
	timestamps_and_patterns = timestamps_array | patterns_array

	new_data = np.zeros(shape=(len(timestamps_array),2)).astype('uint32')

	new_data[:,0] = timestamps_and_patterns >> 32
	new_data[:,1] = timestamps_and_patterns.astype('uint32') 
	# print(new_data)

	new_data.astype('uint32').tofile(outfile)

def read(filename):
    """Reads raw timestamp into time and patterns vectors

    :param filename: a python file object open in binary mode
    :type filename: _io.BufferedReader
    :returns: Two vectors: timestamps, corresponding pattern
    :rtype: {numpy.ndarray(float), numpy.ndarray(uint32)}
    """
    with open(filename, 'rb') as f:
        data = np.fromfile(file=f, dtype='<u4').reshape(-1, 2)
        # cast to uint64!!!
        t = ((np.uint64(data[:, 0]) << 17) + (data[:, 1] >> 15))# / 8. # time in nanoseconds. 
        #t = ((np.uint64(data[:, 0]) << 17) + (data[:, 1] >> 15)) 
        p = data[:, 1] & 0xf
        return t, p

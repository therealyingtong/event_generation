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

	# 2 ^ detector_index
	patterns_array = 2 ** np.asarray([event[1] for event in events_array]) 

	# shift bits and force types
	timestamps_array = timestamps_array.astype('uint64') << 15
	patterns_array = patterns_array.astype('uint32')
	timestamps_and_patterns = timestamps_array | patterns_array

	new_data = np.zeros(shape=(len(timestamps_array),2)).astype('uint32')

	new_data[:,0] = timestamps_and_patterns >> 32

	new_data[:,1] = timestamps_and_patterns.astype('uint32') 

	new_data.astype('uint32').tofile(outfile)

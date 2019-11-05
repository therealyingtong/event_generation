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

def new_merge(a, b):
    if len(a) < len(b):
        b, a = a, b
    c = np.empty(len(a) + len(b), dtype=a.dtype)
    b_indices = np.arange(len(b)) + np.searchsorted(a, b)
    a_indices = np.ones(len(c), dtype=bool)
    a_indices[b_indices] = False
    c[b_indices] = b
    c[a_indices] = a
    return c
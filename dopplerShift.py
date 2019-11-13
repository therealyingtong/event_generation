import numpy as np
import ephem
import astropy as astro
import matplotlib.pyplot as plt
import scipy.constants as constants

def calcDoppler(sat, loc, startTime, timeStamp, units):

	print("calculating Doppler shift")

	s_list = [] # range (range = distance from observer to satellite)

	for stamp in timeStamp:
		d_time = ephem.Date(startTime + (ephem.second * stamp * units))
		loc.date = d_time

		sat.compute(loc)

		s_list.append(sat.range)

	delay_list = [s / (constants.c*units) for s in s_list]

	return delay_list

def propagationDelay(timeStamp, delay_list):

	shiftedTimeStamp = timeStamp.copy()

	for i in range(len(timeStamp)):
		shiftedTimeStamp[i] = timeStamp[i] + delay_list[i]
		# print('shiftedTimeStamp[i], timeStamp[i], delay_list[i]',
		# shiftedTimeStamp[i], timeStamp[i], delay_list[i])
	return shiftedTimeStamp

def clockDriftShift(timeStamp, df_list, clockDrift):

	shiftedTimeStamp = timeStamp.copy()

	for i in range(len(shiftedTimeStamp)):
		t = timeStamp[i] 
		drift = clockDrift
		secondOrderShift = t*(drift + df_list[i])
		shiftedTimeStamp[i] = t + secondOrderShift

	return shiftedTimeStamp

def plotDoppler(timeStamp, df_list, delay_list):

	print("plotting Doppler shift")

	plt.figure()
	plt.plot(timeStamp, df_list)
	# plt.title('Second order Doppler shift')
	plt.xlabel("time (ns)")
	plt.ylabel('second order Doppler shift')
	plt.savefig("../paper/assets/range_velocity.png") 
	plt.close()

	print("plotting Doppler delay")
	plt.figure()
	plt.plot(timeStamp, delay_list)
	# plt.title('Delay due to Doppler shift')
	plt.xlabel("time (ns)")
	plt.ylabel('delay (ns)')
	plt.savefig("../paper/assets/delay.png") 
	plt.close()
#!/usr/bin/env python
# coding: utf-8

import config
import numpy as np
from matplotlib import pyplot as plt
import helper
import dopplerShift as doppler
import helper
import datetime

print('0. read satellite orbit info')
sat, loc, startTime = helper.parseSatellite(config.TLE_path, config.saved_pass_path)

print('1. create timestamps with Poissonian distribution')
arr_times = np.random.exponential(1/config.gen_rate, size=int(config.duration * config.gen_rate) )
timestamps = np.cumsum(arr_times)

print('2. create two copies of timestamps for Alice and Bob')
timestamps_Alice = np.copy(timestamps)
timestamps_Bob = np.copy(timestamps)

# =================================================
# Alice
# =================================================

print('3. introduce dark counts and stray light')
dark_arr_times_Alice = np.random.exponential(1/config.dark_Alice, size=int(config.duration * config.dark_Alice) )
dark_events_Alice = np.cumsum(dark_arr_times_Alice)
timestamps_Alice = helper.new_merge(timestamps_Alice, dark_events_Alice)

print('4. randomly assign randomly assign each event in `timestamps_Alice` to a detector, to form `pattern_Alice`')
patterns_Alice = np.random.randint(0, config.n_detectors, size=len(timestamps_Alice))

print('5. drop a fraction of events according to each detector efficiency')

detected_indices = []
for i in range(len(config.eta_Alice)):
	p_drop = config.eta_Alice[i]
	# indices = np.where(patterns_Alice == i)
	indices = np.where(patterns_Alice == i)[0]
	dropped_indices = np.random.choice(len(indices), int(p_drop*len(indices)), replace=False)
	remaining_indices = np.delete(indices, dropped_indices)
	detected_indices = detected_indices + remaining_indices.tolist()

timestamps_Alice = np.take(timestamps_Alice, detected_indices)
patterns_Alice = np.take(patterns_Alice, detected_indices)

print('6. add a delay according to each detector skew')
for i in range(len(patterns_Alice)):
	skew = config.skew_Alice[patterns_Alice[i]]
	timestamps_Alice[i] = timestamps_Alice[i] + skew

print('7. for each detector, remove any timestamp that occurs less than dead_i after the previous event')
print(datetime.datetime.now())
for i in range(1, len(patterns_Alice)):
	dead = config.dead_Alice[patterns_Alice[i]]
	if (patterns_Alice[i] == patterns_Alice[i - 1] and timestamps_Alice[i] <= timestamps_Alice[i - 1] + dead):
		np.delete(patterns_Alice, i)
		np.delete(timestamps_Alice, i)
print(datetime.datetime.now())

print('8. stretch and squeeze using drift_Alice and drift_rate_Alice')
for i in range(len(timestamps_Alice)):
	t = timestamps_Alice[i]
	t_stretched = t*config.drift_Alice + t*t*config.drift_rate_Alice
	timestamps_Alice[i] = t_stretched

# =================================================
# Bob
# =================================================

print('9. drop a fraction of events in timestamps_Bob according to transmission_loss')

p_loss = config.transmission_loss
lost_indices = np.random.choice(len(timestamps_Bob), int(p_drop*len(timestamps_Bob)), replace=False)
timestamps_Bob = np.delete(timestamps_Bob, lost_indices)


print('10. introduce a Doppler shift on timestamps_Bob using the TLE and saved pass metadata')
delay_list, df_list = doppler.calcDoppler(
	sat, loc, startTime, timestamps_Bob, 1
)
timestamps_Bob = timestamps_Bob + np.array(delay_list) 

print ('11. introduce dark counts and stray light (i.e. additional events) in `timestamps_Bob` using `dark_Bob`')
dark_arr_times_Bob = np.random.exponential(1/config.dark_Bob, size=int(config.duration * config.dark_Bob) )
dark_events_Bob = np.cumsum(dark_arr_times_Bob)
timestamps_Bob = helper.new_merge(timestamps_Bob, dark_events_Bob)

print('12. randomly assign each event in `timestamps_Bob` to a detector, to form `pattern_Bob`')
patterns_Bob = np.random.randint(0, config.n_detectors, size=len(timestamps_Bob))

print('13. for each of Bobs detectors, drop a fraction of events at random according to the detectors efficiency, `eta_i`')
detected_indices = []
for i in range(len(config.eta_Bob)):
	p_drop = config.eta_Bob[i]
	# indices = np.where(patterns_Alice == i)
	indices = np.where(patterns_Bob == i)[0]
	dropped_indices = np.random.choice(len(indices), int(p_drop*len(indices)), replace=False)
	remaining_indices = np.delete(indices, dropped_indices)
	detected_indices = detected_indices + remaining_indices.tolist()

timestamps_Bob = np.take(timestamps_Bob, detected_indices)
patterns_Bob = np.take(patterns_Bob, detected_indices)

print('14. for each of Bobs detectors, add a delay according to the detectors skew, `skew_i`')
for i in range(len(patterns_Bob)):
	skew = config.skew_Bob[patterns_Bob[i]]
	timestamps_Bob[i] = timestamps_Bob[i] + skew

print('15. for each of Bobs detectors, remove any event that occurs less than `dead_i` after the previous event')
print(datetime.datetime.now())
for i in range(1, len(patterns_Bob)):
	dead = config.dead_Bob[patterns_Bob[i]]
	if (patterns_Bob[i] == patterns_Bob[i - 1] and timestamps_Bob[i] <= timestamps_Bob[i - 1] + dead):
		np.delete(patterns_Bob, i)
		np.delete(timestamps_Bob, i)
print(datetime.datetime.now())

print('16. stretch and squeeze `events_Bob` using `drift_Bob` and `drift_rate_Bob`')
for i in range(len(timestamps_Bob)):
	t = timestamps_Bob[i]
	t_stretched = t*config.drift_Bob + t*t*config.drift_rate_Bob
	timestamps_Bob[i] = t_stretched
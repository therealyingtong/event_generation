#!/usr/bin/env python
# coding: utf-8

import gc
gc.collect()

import config
import numpy as np
from matplotlib import pyplot as plt
import helper
import dopplerShift as doppler
import detector
import datetime

print('0. read satellite orbit info')
sat, loc, startTime = helper.parseSatellite(config.TLE_path, config.saved_pass_path)

print('1. create timestamps with Poissonian distribution')
arr_times = np.random.exponential(1/config.gen_rate, size = int(config.duration * config.gen_rate) )
timestamps = np.cumsum(arr_times)

print('2. create two copies of timestamps for Alice and Bob')
timestamps_Alice = np.copy(timestamps)
timestamps_Bob = np.copy(timestamps)
del timestamps

# =================================================
# Alice
# =================================================

print('3. introduce dark counts and stray light')
dark_arr_times_Alice = np.random.exponential(1/config.dark_Alice, size = int(config.duration * config.dark_Alice) )
dark_events_Alice = np.cumsum(dark_arr_times_Alice)
timestamps_Alice = helper.new_merge(timestamps_Alice, dark_events_Alice)

print('4. randomly assign randomly assign each event in `timestamps_Alice` to a detector, to form `pattern_Alice`')
patterns_Alice = np.random.randint(0, config.n_detectors, size=len(timestamps_Alice))
events_Alice = list(zip(timestamps_Alice, patterns_Alice))
del timestamps_Alice
del patterns_Alice

print('5. drop a fraction of events according to each detector efficiency')
events_Alice = detector.efficiency(
	config.eta_Alice, events_Alice
)

print('6. add a delay according to each detector skew')
events_Alice = detector.skew(
	config.skew_Alice, events_Alice
)

print('7. for each detector, remove any timestamp that occurs less than dead_i after the previous event')
dead_indices = []
events_Alice = detector.dead(
	config.dead_Alice, events_Alice
)

print('8. stretch and squeeze using drift_Alice and drift_rate_Alice')
for i in range(len(events_Alice)):
	t = events_Alice[i][0]
	t_stretched = t*config.drift_Alice + t*t*config.drift_rate_Alice
	events_Alice[i][0] = t_stretched

# =================================================
# Bob
# =================================================

print('9. drop a fraction of events in timestamps_Bob according to transmission_loss')
p_loss = 1 / (10**(config.transmission_loss/10))
lost_indices = np.random.choice(len(timestamps_Bob), int(p_loss*len(timestamps_Bob)), replace=False)
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
events_Bob = list(zip(timestamps_Bob, patterns_Bob))
del timestamps_Bob
del patterns_Bob

print('13. drop a fraction of events according to each detector efficiency')
events_Bob = detector.efficiency(
	config.eta_Bob, events_Bob
)

print('14. add a delay according to each detector skew')
events_Bob = detector.skew(
	config.skew_Bob, events_Bob
)

print('15. for each detector, remove any timestamp that occurs less than dead_i after the previous event')
dead_indices = []
events_Bob = detector.dead(
	config.dead_Bob, events_Bob
)

print('16. stretch and squeeze using drift_Bob and drift_rate_Bob')
for i in range(len(events_Bob)):
	t = events_Bob[i][0]
	t_stretched = t*config.drift_Bob + t*t*config.drift_rate_Bob
	events_Bob[i][0] = t_stretched
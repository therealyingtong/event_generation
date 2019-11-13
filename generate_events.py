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
import time
from operator import add 
import environment

time = str(int(time.time()))

print('0. read satellite orbit info')
sat, loc, startTime = helper.parseSatellite(config.TLE_path, config.saved_pass_path)

print('1. create timestamps with Poissonian distribution for Alice')
arr_times = np.random.exponential(1/config.gen_rate, size = int(config.duration * config.gen_rate) )
timestamps_Alice = np.cumsum(arr_times) 

print('2. randomly assign randomly assign each event in `timestamps_Alice` to a detector, to form `pattern_Alice`')
patterns_Alice = np.random.randint(0, config.n_detectors, size=len(timestamps_Alice), dtype = 'uint8')
events_Alice = list(zip(timestamps_Alice, patterns_Alice))
del timestamps_Alice
del patterns_Alice

print('3. create a copy of events_Alice for Bob')
events_Bob = events_Alice.copy()

# =================================================
# Alice
# =================================================

print('4. introduce dark counts and stray light for Alice')
events_Alice = environment.dark_count(config.dark_Alice, config.n_detectors, config.duration, events_Alice)

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

print('======== write events_Alice to outfile ========')
outfile_Alice ="./data/alice" + time + ".bin"
helper.write(config.tau_res, outfile_Alice, events_Alice)
del events_Alice

# =================================================
# Bob
# =================================================

print('9. drop a fraction of events in events_Bob according to transmission_loss')
timestamps_Bob = [event[0] for event in events_Bob]
patterns_Bob = [event[1] for event in events_Bob]
del events_Bob

timestamps_Bob, patterns_Bob = environment.transmission(config.transmission_loss, timestamps_Bob, patterns_Bob)

print('10. introduce a Doppler shift on timestamps_Bob using the TLE and saved pass metadata')
delay_list = doppler.calcDoppler(
	sat, loc, startTime, timestamps_Bob, 1
)
timestamps_Bob = [sum(x) for x in zip(timestamps_Bob, delay_list)]
del delay_list

print('11. randomly select same or different bases for Bob, and assign detectors')

# indices with different bases (half of them)
diff_indices = 	np.random.choice(len(patterns_Bob), int(0.5*len(patterns_Bob)), replace=False)
diff_0_indices_indices = np.random.choice(len(diff_indices), int(0.5*len(diff_indices)), replace=False)
diff_0_indices = np.take(diff_indices, diff_0_indices_indices)
diff_1_indices = np.delete(diff_indices, diff_0_indices_indices)
del diff_indices

for i in range(len(diff_0_indices)):
	patterns_Bob[i] = (bool(np.floor(patterns_Bob[i] / 2) ) ^ bool(1))*2 
for i in range(len(diff_1_indices)):
	patterns_Bob[i] = (bool(np.floor(patterns_Bob[i] / 2) ) ^ bool(1))*2 + 1

events_Bob = list(zip(timestamps_Bob, patterns_Bob))
del timestamps_Bob
del patterns_Bob

print ('12. introduce dark counts and stray light (i.e. additional events) in `timestamps_Bob` using `dark_Bob`')
events_Bob = environment.dark_count(config.dark_Bob, config.n_detectors, config.duration, events_Bob)

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


print('17. write events_Bob to outfiles')
outfile_Bob ="./data/bob" + time + ".bin"
helper.write(config.tau_res, outfile_Bob, events_Bob)


#!/usr/bin/env python
# coding: utf-8

# garbage collector for unused variables
import gc
gc.collect()
import sys

# python libraries
import numpy as np
from matplotlib import pyplot as plt
import time
from operator import add 

zeroConfig = sys.argv[1]
if zeroConfig:
	import zero_config as config
else:
	import config
# modules in this project
import parser
import dopplerShift as doppler
import detector
import environment

# mark current time for unique naming of outfiles
time = str(int(time.time()))

print('0. read satellite orbit info')
sat, loc, startTime = parser.parseSatellite(config.TLE_path, config.saved_pass_path)

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
print('len(events_Alice)', len(events_Alice))

# =================================================
# Alice
# =================================================

print('4. introduce dark counts and stray light (i.e. additional events) in `events_Alice` using `dark_Alice`')
events_Alice = environment.dark_count(
	config.dark_Alice, config.n_detectors, config.duration, events_Alice
)
print('len(events_Alice)', len(events_Alice))

print('5. drop a fraction of events according to each detector efficiency')
events_Alice = detector.efficiency(
	config.eta_Alice, events_Alice
)
print('len(events_Alice)', len(events_Alice))

print('6. add a delay according to each detector skew')
events_Alice = detector.skew(
	config.skew_Alice, events_Alice
)
print('len(events_Alice)', len(events_Alice))

print('7. for each detector, remove any timestamp that occurs less than dead_i after the previous event')
events_Alice = detector.dead(
	config.dead_Alice, events_Alice
)
print('len(events_Alice)', len(events_Alice))

print('8. stretch and squeeze using drift_Alice and drift_rate_Alice')
timestamps_Alice = [event[0] for event in events_Alice]
patterns_Alice = [event[1] for event in events_Alice]
del events_Alice
for i in range(len(timestamps_Alice)):
	t = timestamps_Alice[i]
	t_stretched = t + t*config.drift_Alice + t*t*config.drift_rate_Alice
	timestamps_Alice[i] = t_stretched

print('======== write events_Alice to outfile ========')
outfile_Alice ="./data/alice_" + str(int(config.gen_rate)) + "_" + str(int(config.duration)) + ".bin"
parser.write(
	config.tau_res, outfile_Alice, list(zip(timestamps_Alice, patterns_Alice))
)

del timestamps_Alice
del patterns_Alice

# =================================================
# Bob
# =================================================

print('9. drop a fraction of events in events_Bob according to transmission_loss')
timestamps_Bob = [event[0] for event in events_Bob]
patterns_Bob = [event[1] for event in events_Bob]
del events_Bob

# print('timestamps_Bob[0:50]', timestamps_Bob[0:50])


print('len(timestamps_Bob) before transmission loss', len(timestamps_Bob))
timestamps_Bob, patterns_Bob = environment.transmission(
	config.transmission_loss, timestamps_Bob, patterns_Bob
)
print('len(timestamps_Bob) after transmission loss', len(timestamps_Bob))

if config.doppler:
	print('10. introduce a Doppler shift on timestamps_Bob using the TLE and saved pass metadata')
	delay_list = doppler.calcDoppler(
		sat, loc, startTime, timestamps_Bob, 1
	)
	timestamps_Bob = [sum(x) for x in zip(timestamps_Bob, delay_list)]
	del delay_list

print('11. randomly select same or different bases for Bob, and assign detectors')

# indices with different bases (half of them)
diff_indices = 	np.random.choice(len(patterns_Bob), int(0.5*len(patterns_Bob)), replace=False)

# indices with different basis and |0> result
diff_0_indices_indices = np.random.choice(len(diff_indices), int(0.5*len(diff_indices)), replace=False)
diff_0_indices = np.take(diff_indices, diff_0_indices_indices)

for i in range(len(diff_0_indices)):
	patterns_Bob[diff_0_indices[i]] = int(bool(np.floor(patterns_Bob[i] / 2) ) ^ bool(1))*2 

# indices with different basis and |1> result
diff_1_indices = np.delete(diff_indices, diff_0_indices_indices)
for i in range(len(diff_1_indices)):
	patterns_Bob[diff_1_indices[i]] = int(bool(np.floor(patterns_Bob[i] / 2) ) ^ bool(1))*2 + 1

del diff_indices

events_Bob = list(zip(timestamps_Bob, patterns_Bob))
del timestamps_Bob
del patterns_Bob

print ('12. introduce dark counts and stray light (i.e. additional events) in `timestamps_Bob` using `dark_Bob`')
events_Bob = environment.dark_count(config.dark_Bob, config.n_detectors, config.duration, events_Bob)
print('len(events_Bob)', len(events_Bob))

print('13. drop a fraction of events according to each detector efficiency')
events_Bob = detector.efficiency(
	config.eta_Bob, events_Bob
)
print('len(events_Bob)', len(events_Bob))

print('14. add a delay according to each detector skew')
events_Bob = detector.skew(
	config.skew_Bob, events_Bob
)

print('15. for each detector, remove any timestamp that occurs less than dead_i after the previous event')
dead_indices = []
events_Bob = detector.dead(
	config.dead_Bob, events_Bob
)
print('len(events_Bob)', len(events_Bob))

print('16. stretch and squeeze using drift_Bob and drift_rate_Bob')
timestamps_Bob = [event[0] for event in events_Bob]
patterns_Bob = [event[1] for event in events_Bob]
del events_Bob
for i in range(len(timestamps_Bob)):
	t = timestamps_Bob[i]
	t_stretched = t + t*config.drift_Bob + t*t*config.drift_rate_Bob
	timestamps_Bob[i] = t_stretched

print('========== write events_Bob to outfiles ==========')
print('len(timestamps_Bob), len(patterns_Bob)', len(timestamps_Bob), len(patterns_Bob))
outfile_Bob ="./data/bob_" + str(int(config.gen_rate)) + "_" + str(int(config.duration)) + ".bin"

parser.write(config.tau_res, outfile_Bob, list(zip(timestamps_Bob, patterns_Bob)))


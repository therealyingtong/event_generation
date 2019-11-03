#!/usr/bin/env python
# coding: utf-8

import config
import numpy as np
from matplotlib import pyplot as plt
import helper

outfile="sim_data/2million.bin"

# 1. create events with Poissonian distribution
arr_times = np.random.exponential(1/config.gen_rate, size=int(config.duration * config.gen_rate) )
events = np.cumsum(arr_times)

# 2. create two copies of events for Alice and Bob
events_Alice = np.copy(events)
events_Bob = np.copy(events)

# =================================================
# for events_Alice
# =================================================

# 3. introduce dark counts and stray light
dark_arr_times = np.random.exponential(1/config.dark_Alice, size=int(config.duration * config.dark_Alice) )
dark_events = np.cumsum(dark_arr_times)
events = helper.new_merge(events, dark_events)

# 4. randomly assign each event to a detector and measurement result

# 5. drop a fraction of events according to each detector's efficiency



s = np.copy(arr_times)
dead_time_condition_Alice = s > 1e-9

good_events = np.extract(dead_time_condition_Alice,s)
event_timestamps_s = np.cumsum(good_events)

q=np.random.randint(0,4,size=len(event_timestamps_s))

p = 2**q

t = event_timestamps_s /0.125e-9

t_u64 = t.astype('uint64')

new_data = np.zeros(t_u64.shape,dtype='uint32')

t_shifted = t_u64 <<15

t_timestamp_and_event = t_shifted | p.astype('uint64')

new_data =np.zeros(shape=(len(t),2)).astype('uint32')
print(new_data)

# # In[149]:

# new_data[:,0] = t_timestamp_and_event >> 32

# # In[150]:

# new_data[:,1] = t_timestamp_and_event.astype('uint32') 

# # In[151]:

# new_data.astype('uint32').tofile(outfile)

# print("number of events generated: ", len(event_timestamps_s) )
# print("duration: ", event_timestamps_s[-1], " seconds")

# def _data_extractor(filename):
#     """Reads raw timestamp into time and patterns vectors

#     :param filename: a python file object open in binary mode
#     :type filename: _io.BufferedReader
#     :returns: Two vectors: timestamps, corresponding pattern
#     :rtype: {numpy.ndarray(float), numpy.ndarray(uint32)}
#     """
#     with open(filename, 'rb') as f:
#         data = np.fromfile(file=f, dtype='<u4').reshape(-1, 2)
#         # cast to uint64!!!
#         t = ((np.uint64(data[:, 0]) << 17) + (data[:, 1] >> 15))# / 8. # time in nanoseconds. 
#         #t = ((np.uint64(data[:, 0]) << 17) + (data[:, 1] >> 15)) 
#         p = data[:, 1] & 0xf
#         return t, p


# # In[157]:

# #tt,pp = _data_extractor("sim_data/1million.bin")




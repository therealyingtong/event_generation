#!/usr/bin/env python
# coding: utf-8

import numpy as np
s = np.random.exponential(1e-6, size=int(1e6 *1.2 ) )

outfile="data/2million.bin"

dead_time_s = 150e-9

dead_time_condition = s>dead_time_s

good_events = np.extract(dead_time_condition,s)

event_timestamps_s = np.cumsum(good_events)

q=np.random.randint(0,4,size=len(event_timestamps_s))

p = 2**q

t = event_timestamps_s /0.125e-9

t_u64 = t.astype('uint64')

t_shifted = t_u64 <<15

# new_data = np.zeros(t_u64.shape,dtype='uint32')

t_timestamp_and_event = t_shifted | p.astype('uint64')

print(t_timestamp_and_event[0:100])

new_data =np.zeros(shape=(len(t),2)).astype('uint32')

new_data[:,0] = t_timestamp_and_event >> 32

new_data[:,1] = t_timestamp_and_event.astype('uint32') 

print(new_data[0:50])

new_data.astype('uint32').tofile(outfile)

print("number of events generated: ", len(event_timestamps_s) )
print("duration: ", event_timestamps_s[-1], " seconds")

def _data_extractor(filename):
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

#tt,pp = _data_extractor("sim_data/1million.bin")




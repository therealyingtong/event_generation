import numpy as np
import parser

s = np.random.exponential(1e-6, size=int(1e6 *1.2 ) )
dead_time_s = 150e-9
dead_time_condition = s>dead_time_s
good_events = np.extract(dead_time_condition,s)
event_timestamps_s = np.cumsum(good_events)
p = np.random.randint(0,4,size=len(event_timestamps_s))
t = event_timestamps_s 

print(t[0:100])
print(p[0:100])

events = list(zip(t, p))
parser.write(0.125e-9, './data/2million_test.bin', events)
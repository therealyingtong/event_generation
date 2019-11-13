import numpy as np

def dark_count(dark_count_rate, n_detectors, duration, events):
	dark_arr_times = np.random.exponential(1/dark_count_rate, size = int(duration * dark_count_rate) )
	dark_timestamps = np.cumsum(dark_arr_times)
	dark_patterns = np.random.randint(0, n_detectors, size=len(dark_timestamps), dtype = 'uint8')
	dark_events = list(zip(dark_timestamps, dark_patterns))
	del dark_timestamps
	del dark_patterns

	events = sorted((events + dark_events), key = lambda tup: tup[0])

	return events

def transmission(transmission_loss, timestamps, patterns):
	p_loss = 1 / (10**(transmission_loss/10))
	lost_indices = np.random.choice(len(timestamps), int(p_loss*len(timestamps)), replace=False)

	np.delete(timestamps, lost_indices)
	np.delete(patterns, lost_indices)

	return timestamps, patterns
import numpy as np 

def efficiency(eta_array, events_array):
	timestamps_array = [event[0] for event in events_array]
	patterns_array = [event[1] for event in events_array]
	del events_array

	dropped_indices = []
	for i in range(len(eta_array)):
		p_drop = eta_array[i]
		indices = np.where(np.asarray(patterns_array) == i)
		dropped_indices = dropped_indices + np.random.choice(len(indices), int(p_drop*len(indices)), replace=False).tolist()

	timestamps_array = np.delete(timestamps_array, dropped_indices)
	patterns_array = np.delete(patterns_array, dropped_indices)

	return list(zip(timestamps_array, patterns_array))

def skew(skew_array, events_array):
	timestamps_array = [event[0] for event in events_array]
	patterns_array = [event[1] for event in events_array]
	del events_array
	
	for i in range(len(patterns_array)):
		skew = skew_array[patterns_array[i]]
		timestamps_array[i] = timestamps_array[i] + skew

	return list(zip(timestamps_array, patterns_array))

def dead(dead_array, events_array):
	timestamps_array = [event[0] for event in events_array]
	patterns_array = [event[1] for event in events_array]
	del events_array

	dead_indices = []
	for i in range(1, len(patterns_array)):
		dead = dead_array[patterns_array[i]]
		if (
			patterns_array[i] == patterns_array[i - 1] and 
			timestamps_array[i] <= timestamps_array[i - 1] + dead):
			dead_indices.append(i)

	np.delete(timestamps_array, dead_indices)
	np.delete(patterns_array, dead_indices)

	return list(zip(timestamps_array, patterns_array))
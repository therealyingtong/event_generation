import numpy as np 

def efficiency(eta_array, events_array):
	timestamps_array = [event[0] for event in events_array]
	patterns_array = [event[1] for event in events_array]

	detected_indices = []
	for i in range(len(eta_array)):
		p_drop = eta_array[i]
		# indices = np.where(patterns_Alice == i)
		indices = np.where(patterns_array == i)[0]
		dropped_indices = np.random.choice(len(indices), int(p_drop*len(indices)), replace=False)
		remaining_indices = np.delete(indices, dropped_indices)
		detected_indices = detected_indices + remaining_indices.tolist()

	timestamps_array = np.take(timestamps_array, detected_indices)
	patterns_array = np.take(patterns_array, detected_indices)

	return list(zip(timestamps_array, events_array))

def skew(skew_array, events_array):
	timestamps_array = [event[0] for event in events_array]
	patterns_array = [event[1] for event in events_array]
	for i in range(len(patterns_array)):
		skew = skew_array[patterns_array[i]]
		timestamps_array[i] = timestamps_array[i] + skew

	return list(zip(timestamps_array, events_array))

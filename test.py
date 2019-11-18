import numpy as np
import helper

filename_Alice = "data/alice_1574045702.bin"
filename_Bob = "data/bob_1574045702.bin"

timestamps_Alice, patterns_Alice = helper.read(filename_Alice)
timestamps_Bob, patterns_Bob = helper.read(filename_Bob)

filename_Alice_ref = "data/ALICE_12Apr_19_3"
filename_Bob_ref = "data/BOB_12Apr_19_3"

timestamps_Alice_ref, patterns_Alice_ref = helper.read(filename_Alice_ref)
timestamps_Bob_ref, patterns_Bob_ref = helper.read(filename_Bob_ref)

print('len(timestamps_Alice)', len(timestamps_Alice))
print('len(timestamps_Alice_ref)', len(timestamps_Alice_ref))
print('len(timestamps_Bob)', len(timestamps_Bob))
print('len(timestamps_Bob_ref)', len(timestamps_Bob_ref))
import qcrypto_helper
import config
import sys
import os

alice_readevent_file =  sys.argv[1]
bob_readevent_file =  sys.argv[2]
remotecrypto_folder = sys.argv[3]
errorcorrection_folder = sys.argv[4]

# global variables
process_time_limit = 5 # seconds
processed_data_root = config.processed_data_root

# create folders for processed data
alice_folder = processed_data_root + "/alice"
bob_folder = processed_data_root + "/bob"

alice_t1 = alice_folder + "/t1"
alice_t3 = alice_folder + "/t3"
alice_t4 = alice_folder + "/t4"
alice_t7 = alice_folder + "/t7"

bob_t2 = bob_folder + "/t2"
bob_t3_outcome = bob_folder + "/t3_outcome"
bob_t5 = bob_folder + "/t5"
bob_t3_rawkey = bob_folder + "/t3_rawkey"
bob_t7 = bob_folder + "/t7"
 
qcrypto_helper.create_data_folders(
	processed_data_root, 
	[alice_folder, alice_t1, alice_t3, alice_t4, alice_t7, 
	bob_folder, bob_t2, bob_t3_outcome, bob_t5, bob_t3_rawkey, bob_t7]
)

# log commands
qcrypto_helper.log(processed_data_root)

# chopper on Bob's data, saves private outcome in t3, saves public basis and timestamp in t2
qcrypto_helper.chop_bob(bob_readevent_file, bob_t2, bob_t3_outcome, remotecrypto_folder)

# chopper2 on Alice's data, saves info in t1
qcrypto_helper.chop2_alice(alice_readevent_file, alice_t1, remotecrypto_folder)

# p_find using Alice's data and Bob's transmitted public data
first_epoch = str(os.listdir(alice_t1)[0])
num_epochs = len(os.listdir(alice_t1)) - 2

qcrypto_helper.p_find(first_epoch, num_epochs, alice_t1, bob_t2, remotecrypto_folder) 

## TODO: get diff from C fprintf
diff = -1965472

# costream to get Alice's raw key (t3) and coincidence events (t4)
qcrypto_helper.co_stream(first_epoch, diff, num_epochs - 1, alice_t1, alice_t3, alice_t4, bob_t2, remotecrypto_folder)

# splicer on Bob's side
qcrypto_helper.splicer(bob_t3_outcome, alice_t4, bob_t5, bob_t3_rawkey, first_epoch, num_epochs - 1, remotecrypto_folder)

# ecd2 Alice

# ecd2 Bob


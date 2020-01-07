import qcrypto_helper
import config
import sys
import os

alice_readevent_file =  sys.argv[1]
bob_readevent_file =  sys.argv[2]
remotecrypto_folder = sys.argv[3]
errorcorrection_folder = sys.argv[4]
alice_ip = config.alice_ip 
alice_port = config.alice_port
bob_ip = config.bob_ip
bob_port = config.bob_port

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
alice_notif = alice_folder + "/notif.txt"
alice_query = alice_folder + "/query.txt"
alice_respond = alice_folder + "/respond.txt"

bob_t2 = bob_folder + "/t2"
bob_t3_outcome = bob_folder + "/t3_outcome"
bob_t5 = bob_folder + "/t5"
bob_t3_rawkey = bob_folder + "/t3_rawkey"
bob_t7 = bob_folder + "/t7"
bob_notif = bob_folder + "/notif.txt"
bob_query = bob_folder + "/query.txt"
bob_respond = bob_folder + "/respond.txt"

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

# transferd on Alice's side
alice_command = "alice_command"
alice_ec_in = "alice_ec_in"
alice_ec_out = "alice_ec_out"
alice_transferd_log = alice_folder + "alice_transferd_log"

qcrypto_helper.transferd(
	alice_folder, alice_command, bob_ip, bob_folder, alice_transferd_log, alice_ec_in, alice_ec_out, alice_port, remotecrypto_folder
)

# transferd on Bob's side
bob_command = "bob_command"
bob_ec_in = "bob_ec_in"
bob_ec_out = "bob_ec_out"
bob_transferd_log = bob_folder + "bob_transferd_log"

qcrypto_helper.transferd(
	bob_folder, bob_command, alice_ip, bob_folder, bob_transferd_log, bob_ec_in, bob_ec_out, bob_port, remotecrypto_folder
)


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


# # ecd2 Alice
# num_blocks = 5
# commandpipe = "echo " + str(first_epoch) + " " + str(num_blocks) + " \0"
# sendpipe = "binary connection which reaches to the transfer program"
# receivepipe = "same as sendpipe, but for incoming packets"
# rawkeydirectory = alice_t3
# finalkeydirectory = alice_t7
# notificationpipe = alice_notif
# querypipe = alice_query
# respondpipe = alice_respond

# qcrypto_helper.ecd2(commandpipe, sendpipe, receivepipe, rawkeydirectory, finalkeydirectory, notificationpipe, querypipe, respondpipe, errorcorrection_folder)

# # ecd2 Bob


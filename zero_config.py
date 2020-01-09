doppler = False

# ================================================
# SOURCE CONFIG
# ================================================

gen_rate = 1e2 # event generation rate in counts/second
duration = 50 # duration of event generation in seconds
# stress testing: 300s
# test: 5s
n_detectors = 4 # number of detectors for EACH Alice and Bob

# ================================================
# METADATA
# ================================================
TLE_path = "./data/GALASSIA-TLE.txt"
saved_pass_path = "./data/GALASSIA-15723-pass-48.txt"
processed_data_root = "./" + str(int(gen_rate)) + "_" + str(int(duration))
remotecrypto_folder = "../qcrypto/remotecrypto"
errorcorrection_folder = "../qcrypto/errorcorrection"
alice_ip = "127.0.0.1"
bob_ip = "127.0.0.1"
alice_port = "4852"
bob_port = "4855"

# ================================================
# ZERO CONFIG
# ================================================

eta_Alice = [1,1,1,1] # detector efficiencies for Alice
skew_Alice = [0,0,0,0] # detector skews for Alice in s
dead_Alice = [0,0,0,0] # detector dead times for Alice in s

eta_Bob = [1,1,1,1] # detector efficiencies for Bob
skew_Bob = [0,0,0,0] # detector skews for Bob in s
dead_Bob = [0,0,0,0] # detector dead times for Bob in s

tau_res = 0.125e-9 # timestamp resolution in s
tau = 2e-9 # coincidence window in s

drift_Alice = 0 # Alice average clock drift in s/s
drift_rate_Alice = 0 # Alice average clock drift rate in s/s^2

drift_Bob = 0  # Bob average clock drift in s/s
drift_rate_Bob = 0  # Bob average clock drift rate in s/s^2

transmission_loss = 10 # transmission loss in dB
dark_Alice = 1 # dark count rates for Alice in counts/s
dark_Bob = 1 # dark count rates for Bob in counts/s

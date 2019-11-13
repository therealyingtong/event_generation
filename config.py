# ================================================
# SOURCE CONFIG
# ================================================

gen_rate = 16e6 # event generation rate in counts/second
duration = 1 # duration of event generation in seconds
n_detectors = 4 # number of detectors for EACH Alice and Bob

# ================================================
# DETECTOR CONFIG
# ================================================

# Alice
eta_Alice = [0.25,0.25,0.25,0.25] # detector efficiencies for Alice
skew_Alice = [0,0,0,0] # detector skews for Alice in s
dead_Alice = [100e-9,100e-9,100e-9,100e-9] # detector dead times for Alice in s

# Bob
eta_Bob = [0.25,0.25,0.25,0.25] # detector efficiencies for Bob
skew_Bob = [0,0,0,0] # detector skews for Bob in s
dead_Bob = [100e-9,100e-9,100e-9,100e-9] # detector dead times for Bob in s

# ================================================
# CLOCK CONFIG
# ================================================

tau_res = (1e-9)/8 # timestamp resolution in s
tau = 2e-9 # coincidence window in s

drift_Alice = 0.1 # Alice average clock drift in s/s
drift_rate_Alice = 0.01 # Alice average clock drift rate in s/s^2

drift_Bob = 0.1  # Bob average clock drift in s/s
drift_rate_Bob = 0.01  # Bob average clock drift rate in s/s^2

# ================================================
# ENVIRONMENT CONFIG
# ================================================
transmission_loss = 30 # transmission loss in dB
dark_Alice = 3000 # dark count rates for Alice in counts/s
dark_Bob = 3000 # dark count rates for Bob in counts/s

# ================================================
# METADATA
# ================================================
TLE_path = "./data/GALASSIA-TLE.txt"
saved_pass_path = "./data/GALASSIA-15723-pass-48.txt"
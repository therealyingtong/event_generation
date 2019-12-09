import os
import subprocess

printlog = True
process_time_limit = 5 # seconds
processed_data_root = "./TT06Dec_1M_4s"

timestamp_location = "./data"
#timestamp_location = "./shift-coin-data"

alice_readevent_file =  timestamp_location+"/alice_1575870026.bin"

bob_readevent_file =  timestamp_location+ "/bob_1575870026.bin"
alice_folder = processed_data_root + "/alice"
bob_folder = processed_data_root + "/bob"

alice_t1 = alice_folder+"/t1"
alice_t3 = alice_folder+"/t3"
alice_t4 = alice_folder+"/t4"

bob_t2 = bob_folder+"/t2"
bob_t3 = bob_folder+"/t3"

remotecrypto_folder = "../qcrypto/remotecrypto"

chopper = remotecrypto_folder+"/chopper"

def create_data_folders():
    
    if os.path.exists(processed_data_root):
        print ("conflict with existing data folder.",
                "please provide a new data root folder name")
        return False
    else:
        os.mkdir(processed_data_root)
        print ("data root created.")
        
    
    os.mkdir(alice_folder)
    os.mkdir(bob_folder)
    os.mkdir(alice_t1)
    os.mkdir(alice_t3)
    os.mkdir(alice_t4)
    
    os.mkdir(bob_t2)
    os.mkdir(bob_t3)
    print ("data sub directories created.")
    
    return True
    

create_data_folders()
log_file = open(processed_data_root+"/log.txt", "w")
def log(s):
    if printlog is True:
        print(str(s))
    log_file.write(str(s)+'\n')
    log_file.flush()

log(processed_data_root)

def run_sub_process(command, timelimit):
    log("running:"+ command)
    
    process = subprocess.Popen([command], shell=True)
    try:
        log('Running in process:'+str( process.pid))
        #print('Running in process', process.pid)
        process.wait(timeout=timelimit)
    except subprocess.TimeoutExpired:
        log('Timed out - killing'+ str(process.pid) )
        #print('Timed out - killing', process.pid)
        process.kill()
    log("Done")

def chop_bob():
    log("chopper on bob readevent files")
    log("at :"+ bob_readevent_file)
    chop_bob_command = remotecrypto_folder+"/chopper -i "+ bob_readevent_file+" -D "+bob_t2 +" -d "+bob_t3 + " -U"
    run_sub_process(chop_bob_command,process_time_limit)
    
chop_bob()

def chop2_alice():
    log("chopper2 on Alice readevent files")
    log("at :"+ alice_readevent_file)
    chop2_alice_command = remotecrypto_folder+"/chopper2 -i "+ alice_readevent_file+" -D "+alice_t1+" -U "
    log(chop2_alice_command)
    #run_sub_process(chop2_alice_command,process_time_limit)
    os.system(chop2_alice_command)
    #print (chop2_alice_command)

chop2_alice()

def p_find(epoch):
    if "0x" not in epoch.lower():
        xepoch = "0x"+str(epoch)
    log ("running pfind")
    pfind_command = remotecrypto_folder+"/pfind -D "+alice_t1+" -e "\
        + str(xepoch)+ " -d " + bob_t2 + " -r 2 -n 10 -V 3 -q 22"
    log (pfind_command)
    os.system(pfind_command)

p_find("aef40000") # aca2a07a

def p_find_blurb(epoch):
    if "0x" not in epoch.lower():
        xepoch = "0x"+str(epoch)
    log ("running pfind")
    pfindB_command = remotecrypto_folder+"/pfindblurb -D "+alice_t1+" -e "\
        + str(xepoch)+ " -d " + bob_t2 + " -r 2 -n 10 -V 3 -q 20"
    log (pfindB_command)
    os.system(pfindB_command)

def co_stream(epoch,t_diff):
    if "0x" not in epoch.lower():
        xepoch = "0x"+str(epoch)
    log ("running costream")
    costream_command = remotecrypto_folder+"/costream -D "+alice_t1 \
        + " -d "+ bob_t2 + " -F " + alice_t4+" -f " + alice_t3 \
        + " -e " + str(xepoch) + " -w 16 -u 40-p 1 -q 10 -t " + str(t_diff) + "-T 0 -V 4 -G 3"
    log(costream_command)
    os.system(costream_command)
    
co_stream("aef40000", -1965472)

log_file.close()
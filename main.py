import time
import random
import firestore_util
import os
import glob

# list of past temperature readings 
temp_list = []
sample_count = 6

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def average(list):
    return sum(list) / len(list)

# temperature reading loop that posts to server every minute
def start():
    # loop that reads temp on loop
    while(True):
        time.sleep(1)
        # read sensor here
        next_temp = read_temp()
        temp_list.append(next_temp)
        print(f"temp_list = {temp_list}")

        # get average and post reading, then clear list for next reading sample
        if len(temp_list) >= sample_count:
            avg_temp = average(temp_list)
            post_reading(avg_temp)

            print("Dropping all elements from list")
            temp_list.clear()
            

# post reading to server
def post_reading(reading):
    print(f"Posting avg reading {reading}")
    timestamp = time.time()
    firestore_util.set_current_temp(reading, timestamp)
    firestore_util.update_logs(reading, timestamp)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

if __name__ =="__main__":
    start()
import time
import random
import firestore_util

# list of past temperature readings 
temp_list = []
sample_count = 6

def average(list):
    return sum(list) / len(list)

# temperature reading loop that posts to server every minute
def read_temp():
    # loop that reads temp on loop
    while(True):
        time.sleep(1)
        # TODO read sensor here
        next_temp = random.randrange(50, 220)
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

if __name__ =="__main__":
    read_temp()
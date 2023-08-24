import time
print(time.time())

def getTime(time1=0):
    if not time1:
        print(time1)
        return time.time()
    else:
        interval = time.time() - time1
        return time.time(), interval


start_time = getTime()
print(start_time)
print(getTime(start_time))
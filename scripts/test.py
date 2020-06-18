from env import ABM
import time

obj = ABM()
start = time.time()
obj.episode()
end = time.time()
print("Time lapse: {}".format(end-start))
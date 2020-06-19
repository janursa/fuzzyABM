from env import ABM
import time

obj = ABM(run_mode = "test")
start = time.time()
obj.episode()
end = time.time()
print("Time lapse: {}".format(end-start))
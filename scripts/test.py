from env import ABM
import time

obj = ABM(run_mode="test")
obj.reset()
start = time.time()
obj.episode()
end = time.time()
print("Time lapse: {}".format(end-start))
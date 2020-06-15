from env import myEnv_
import time

obj = myEnv_()
obj.setup()
start = time.time()
obj.episode()
end = time.time()
print("Time lapse: {}".format(end-start))
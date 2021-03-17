import time
import sys
import os,sys
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
ABM_path = os.path.join(current_file,'ABM')
sys.path.insert(0,ABM_path)
from env import ABM
data_path = os.path.join(current_file,'..','bio_data')
sys.path.insert(0,data_path)
from observations import observations


scale_factor = observations["scale"]
training_item = ABM.scale(observations["H2017_Mg0"],scale_factor)

try:
    obj = ABM(free_params = {},run_mode="test")
except ValueError as vl:
    print(vl)
    sys.exit(2)

start = time.time()
results,errors,mean_error = obj.episode(trainingItem = training_item)
#print(results)
end = time.time()
print("Time lapse: {}".format(end-start))
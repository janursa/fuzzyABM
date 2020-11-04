from env import ABM, trainingData
import time
import sys
import os,sys
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
medians_path = os.path.join(current_file,'..','outputs_ber','medians.json')
import json


scale_factor = trainingData["scale"]
training_item = ABM.scale(trainingData["H2017_Mg0"],scale_factor)

try:
    obj = ABM(free_params = {},run_mode="test")
except ValueError as vl:
    print(vl)
    sys.exit(2)

start = time.time()
results,errors,mean_error = obj.episode(trainingItem = training_item)
print(results)
end = time.time()
print("Time lapse: {}".format(end-start))
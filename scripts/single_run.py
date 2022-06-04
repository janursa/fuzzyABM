import time
import sys
import os,sys
import pathlib
import json
current_file = pathlib.Path(__file__).parent.absolute()
ABM_path = os.path.join(current_file,'ABM')
sys.path.insert(0,ABM_path)
from env import ABM
data_path = os.path.join(current_file,'..','bio_data')
sys.path.insert(0,data_path)
from observations import observations


scale_factor = observations["scale"]
inferred_params_dir = '/Users/matin/Downloads/testProjs/fuzzyABM/results/H/inferred_params.json'
# training_item = ABM.scale(observations["H2017_Mg0"],scale_factor)
training_item = ABM.scale(observations["H2017_Mg0"],scale_factor)
# training_item = ABM.scale(observations["X_1_C"],scale_factor)

with open(inferred_params_dir,'r') as f:
    inferred_params = json.load(f)["params"]
try:
    obj = ABM(free_params = inferred_params,run_mode="test")
except ValueError as vl:
    print(vl)
    sys.exit(2)

start = time.time()
results,errors,mean_error = obj.episode(trainingItem = training_item)
#print(results)
end = time.time()
print("Time lapse: {}".format(end-start))
from env import ABM
import time
import sys
import os
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
medians_path = os.path.join(current_file,'..','build','outputs','medians.json')
import json
# with open(medians_path) as file:
#     medians = json.load(file)["medians"]

obj = ABM(free_params = {},run_mode="test")
obj.reset()
start = time.time()
obj.episode()
end = time.time()
print("Time lapse: {}".format(end-start))
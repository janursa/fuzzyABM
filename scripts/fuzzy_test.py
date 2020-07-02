import sys
import random
import pathlib
import os
import time
current_file_path = pathlib.Path(__file__).parent.absolute()
sys.path.insert(1,os.path.join(current_file_path,'..','..','fuzzy','build'))
from fuzzy import fuzzy
import json

PARAMS_PATH = os.path.join(current_file_path,'params.json')
if __name__ == '__main__':
	## test fuzy model
	with open(PARAMS_PATH) as file:
			params = json.load(file)
	policy = fuzzy("MSC",params)
	policy.tests()

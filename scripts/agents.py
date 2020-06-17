import sys
import random
import pathlib
import os
import time
current_file_path = pathlib.Path(__file__).parent.absolute()
sys.path.insert(1,current_file_path)
# sys.path.insert(1,os.path.join(current_file_path,'..','..','ABM_base','build','binds'))
sys.path.insert(1,os.path.join(current_file_path,'..','build','binds'))

from myBinds import MSC, Dead
sys.path.insert(1,os.path.join(current_file_path,'..','..','fuzzy','build'))
from fuzzy import fuzzy

class Dead_(Dead):
	"""
	This class describes a Dead cell.
	"""
	def __init__(self,env,configs = None, params = None):
		Dead.__init__(self,env = env, class_name = 'Dead')
		self.configs = configs or {}
		self.params = params or {}
		

	def step(self):
		pass


class MSC_(MSC):
	"""
	This class describes a MSC cell.
	"""
	def __init__(self,env, params = None,initial_conditions = None, id = 0):
		MSC.__init__(self,env = env, class_name = 'MSC',  
					params = params, initial_conditions = initial_conditions,
					id = id )
		self.policy = fuzzy("MSC",params)

	def run_policy(self,policy_inputs):
		"""
		Collects policy inputs, executes policy and returns predictions
		"""
		predictions = self.policy.predict(policy_inputs) # fuzzy controller
		return predictions
	
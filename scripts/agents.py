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
sys.path.insert(1,os.path.join(current_file_path,'..','..','RL','RL'))
from policies import MSC_Policy
import numpy as np
from torch.distributions import Categorical

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
					params = params, initial_conditions = initial_conditions)
		try:
			self.policy = fuzzy("MSC",params)
			# self.policy = MSC_Policy()
		except:
			raise ValueError("Policy raise error")
		self.saved_actions = []
		self.saved_rewards = []
		self.previous_checkpoint = 0
	# def step(self):
	# 	policy_inputs = self.collect_policy_inputs()
	# 	probs,state_value = self.run_policy(policy_inputs)
	# 	m = Categorical(probs)
	# 	action = m.sample()
	# 	self.saved_actions.append((m.log_prob(action),state_value))
	# 	if action == 0:
	# 		self.order_move(quiet=True,reset=True)
	# 	elif action == 1:
	# 		self.order_hatch(inherit=True, quiet=True)
	# 	elif action == 2:
	# 		self.order_switch("Dead")
	# 	else:
	# 		raise ValueError("action is not define for more than 2")
	# 	self.saved_actions.append((m.log_prob(action),state_value))
	def run_policy(self,policy_inputs):
		"""
		Collects policy inputs, executes policy and returns predictions
		"""
		predictions= self.policy.predict(policy_inputs) # fuzzy controller
		# predictions,state_value = self.policy.predict(policy_inputs) # NN

		# return predictions,state_value
		return predictions

	# def reward(self):
	# 	# print("iter {} keys {}".format(str(self.env.tick), self.env.errors.keys()))
	# 	if str(self.env.tick) in self.env.errors:
	# 		errors = self.env.errors[str(self.env.tick)]
	# 		error_liveCellCount = errors["liveCellCount"]
	# 		reward = 100*(1- error_liveCellCount)
	# 		for i in range(self.previous_checkpoint,self.env.tick):
	# 			self.saved_rewards.append(reward)
	# 		self.previous_checkpoint = self.env.tick
	# 		print(len(self.saved_rewards))
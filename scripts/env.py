import sys
import random
import time
import pathlib
import os
import json
import pandas as pd
from pprogress import ProgressBar
import numpy as np

current_file_path = pathlib.Path(__file__).parent.absolute()
sys.path.insert(1,current_file_path)
sys.path.insert(1,os.path.join(current_file_path,'..','build','binds'))

from myBinds import myEnv,mesh_tools
from agents import MSC_,Dead_
from patch import myPatch_

SETTINGS_PATH = os.path.join(current_file_path,'settings.json')
PARAMS_PATH = os.path.join(current_file_path,'params.json')
TRAININGDATA_PATH = os.path.join(current_file_path,'ABC','trainingdata.json')

with open(TRAININGDATA_PATH) as file:
	trainingData = json.load(file)

class ABM(myEnv):
	def __init__(self,free_params = {}):
		myEnv.__init__(self)
		## simulation specific
		with open(SETTINGS_PATH) as file:
			self.settings = json.load(file)
		with open(PARAMS_PATH) as file:
			self.params = json.load(file)
		for key,value in free_params.items():
			self.params[key] = value
		self.set_params(self.params) # sends it to c++
		## specific settings
		self.run_mode = "ABC"  ## other options are test and RL
	def initialize(self):
		## default fields
		self._repo = []
		self.patches.clear()
		self.agents.clear()
		## to update
		self.tick = 0
		self.last_tick = 0
		## env data
		self.data = {}
		self.results = {} # results collected for validation
		self.errors = {}
	def reset(self):
		self.initialize()
		try:
			self.setup()
		except Exception as e:
			raise e
	def update_repo(self):
		self._repo[:]= [agent for agent in self._repo if not agent.disappear]
	def generate_agent(self,agent_name):
		if agent_name == 'MSC':
			agent_obj = MSC_(self, params = self.params.copy(),
				initial_conditions = self.settings["setup"]["agents"]["MSC"]["attrs"].copy())
		elif agent_name == 'Dead':
			agent_obj = Dead_(self, configs = self.settings["setup"]["agents"]["Dead"]["attrs"].copy(),
								  params = self.params.copy())
		else:
			print("Generate agent is not defined for '{}'".format(agent_name))
			sys.exit(0)
		self._repo.append(agent_obj)
		self.agents.append(agent_obj)
		return agent_obj
	def generate_patch(self):
		patch_obj = myPatch_(self, initial_conditions = self.settings["setup"]["patch"]["attrs"].copy(),
								  params = self.params.copy())
		self._repo.append(patch_obj)
		return patch_obj
	def setup(self):
		grid_info = self.settings["setup"]["grid"]
		mesh =  mesh_tools.grid(grid_info["x_l"],grid_info["y_l"],grid_info["patch_size"])
		self.setup_domain(mesh)
		## create agents
		agent_counts = self.settings["setup"]["agents"]["n"]
		
		self.setup_agents(agent_counts)
		
		self.update()
	def step(self):

		self.step_patches()
		self.step_agents()	

		self.tick += 1
		self.update()
		pass
	def update(self):
		super().update()
		
		## Either updates or appends a pair of key-value to self.data
		def add(key,value): 
			if key not in self.data:
				self.data[key] = [value]
			elif self.tick > self.last_tick:
			 	self.data[key].append(value)
			else:
				self.data[key][-1] = value
		
		## agent counts
		counts = self.count_agents()
		for key,count in counts.items():
			add (key,count)
		
		## average ph on patches
		pH_mean = self.collect_from_patches("pH")/len(self.patches)
		add("pH",pH_mean)
		
		## output 
		self.output()

		## calculate errors	//rewards
		self.checkpoint()

		## control
		self.last_tick = self.tick
		if len(self.agents) >  len(self.patches):
			print("Agents cannot exceed patches in number")
			sys.exit(0)

	def checkpoint(self):
		"""
		Calculates the simulation results and errors for the given criteria
		"""
		#step 1: check if it's time for  calculation
		#step 2: extract the validation results for the right time point
		#step 3: calculate the simulation counterpart
		#step 3: calculate error in the same structure as settings
		#step 5: return them
		if "expectations" not in self.settings: # no  calculaton is required
			return
		if str(self.tick) not in self.settings["expectations"]: # not the right tick
			return 
		factors = self.settings["expectations"][str(self.tick)]
		errors = {}
		results = {}
		for key,value in factors.items():
			if key == "liveCellCount":
				sim_res = self.data["MSC"][-1] # last count
			elif key == "viability":
				total_cell_count = self.data["MSC"][-1] + self.data["Dead"][-1] 
				sim_res = (float) (self.data["MSC"][-1])/total_cell_count
			else:
				raise Exception("Error is not defined for '{}'".format(key))

			error_value =abs((float)(sim_res - value)/value) 
			# print("\nsim_res {} value {} error_value {}".format(sim_res,value,error_value))
			errors.update({key:error_value})
			results.update({key:sim_res})
		self.errors.update({str(self.tick):errors})
		self.results.update({str(self.tick):results})	

	def episode(self,trainingItem = None):
		"""
		Runs the model for one single training item
		"""
		#step 1: match the training item with settings
		#steo 1.2: add the expections part
		#step 1.3: in `update`, extract the expections
		#step 2: setup and run the model
		#step 3: reset the model
		#step 3: return the simulation results
		
		if trainingItem:
			self.settings["setup"] = trainingItem["setup"]
			self.settings.update({"expectations":trainingItem["expectations"]})
		try :
			self.reset()
		except ValueError as vl:
			raise vl

		self.duration = self.settings["setup"]["exp_duration"]
		self.pb = ProgressBar(self.duration)
		for i in range(self.duration):
			self.step()
			if self.run_mode == "test":
				self.pb.update()
		self.pb.done()

		# calculate mean error
		mm = []
		for key,item in self.errors.items():
			for key2,error in item.items():
				mm.append(error)
		mean_error = np.mean(mm)
		if self.run_mode == "test":
			print("Episode finished")

		return self.results,self.errors,mean_error

	def run(self):
		"""
		Runs the model for all training items
		"""
		#step 1: for each training item, run `episode` 
		#step 2: receive the results and append it to the epoch results
		#step 3: calculate error
		
		mean_errors = []
		IDs = trainingData["IDs"]
		for ID in IDs:
			training_item = trainingData[ID]
			try:
				_,_,mean_error = self.episode(training_item) 
			except ValueError as vl:
				return None
			mean_errors.append(mean_error)
			
		epoch_error = np.mean(mean_errors)
		return epoch_error

	def test(self):
		results = {}
		IDs = trainingData["IDs"]
		for ID in IDs:
			training_item = trainingData[ID]
			try:
				results_episode,_,_ = self.episode(training_item) 
			except ValueError as vl:
				print("\nValueError inside env::test as ",vl)
				return None

			results.update({ID:results_episode})
		return results

	def output(self):
		"""
		Post processing: logging the results to a file
		"""
		# agents on patches as scatter format
		if self.run_mode != "test":
			return 
		def scatter_patch(patches):
			file = open('outputs/scatter.csv','w')
			file.write('x,y,type,size\n')
			for index,patch in patches.items():
				if patch.empty:
					size_ = 2
					type_ = 'nothing'
				else:
					size_ = 10
					type_ = patch.agent.class_name
					
				file.write("{},{},{},{}\n".format(patch.coords[0],
												patch.coords[1],
												type_,
												size_))
			file.close()
		# print_patch(self.patches)
		def scatter_agents(agents):
			file = open('outputs/scatter.csv','w')
			file.write('x,y,type,size\n')
			for agent in agents:
				x,y,z = agent.patch.coords
				type_ = agent.class_name
				size_ = 10	
				file.write("{},{},{},{}\n".format(x,
												y,
												type_,
												size_))
			file.close()
		scatter_agents(self.agents)
		## agent counts 
		df = pd.DataFrame.from_dict(self.data)
		df_agent_counts = df[["MSC","Dead"]]
		df_agent_counts.to_csv('outputs/agents_traj.csv')
		## average pH 
		df_pH = df[["pH"]]
		df_pH.to_csv('outputs/pH.csv')


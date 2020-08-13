import sys
import random
import time
import pathlib
import os
import json
import pandas as pd
import numpy as np
from math import sqrt
import copy
current_file_path = pathlib.Path(__file__).parent.absolute()


from imports import myEnv,grid, grid3, update_progress
from agents import MSC_,Dead_
from patch import myPatch_

SETTINGS_PATH = os.path.join(current_file_path,'settings.json')
PARAMS_PATH = os.path.join(current_file_path,'params.json')
TRAININGDATA_PATH = os.path.join(current_file_path,'trainingdata.json')

with open(TRAININGDATA_PATH) as file:
	trainingData = json.load(file)

class ABM(myEnv):
	def __init__(self,free_params = {},run_mode = "ABC"):
		myEnv.__init__(self)
		## simulation specific
		#with open(SETTINGS_PATH) as file:
			#self.settings = json.load(file)
		#self.settings = ABM.scale(self.settings,self.settings["scale"]);
		with open(PARAMS_PATH) as file:
			self.params = json.load(file)
		for key,value in free_params.items():
			self.params[key] = value
		self.set_params(self.params) # sends it to c++
		self.construct_policy()
		## specific settings
		self.run_mode = run_mode  ## other options are test and RL
		self.medium_change_interval = 60 ## 2.5 days
		try:
			os.mkdir("outputs")
		except:
			pass
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
		self.set_settings(self.settings["setup"]["grid"])
		grid_info = self.settings["setup"]["grid"]
		mesh =  grid(sqrt(grid_info["area"]),sqrt(grid_info["area"]),grid_info["patch_size"],share = True)
		# mesh =  grid3(sqrt(grid_info["area"]),sqrt(grid_info["area"]),grid_info["patch_size"],grid_info["patch_size"],share = True)

		self.setup_domain(mesh)
		## create agents
		agent_counts = self.settings["setup"]["agents"]["n"]
		self.setup_agents(agent_counts)
		self.update()
	def step(self):
		self.tick += 1
		self.step_patches()
		self.step_agents()
		self.update()

	def update(self):
		super().update()
		if (self.tick % self.medium_change_interval == 0): # medium chaneg
			self.refresh()
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
		## BMP
		BMP = self.collect_from_patches("BMP")
		add("BMP",BMP)
		## TGF
		TGF = self.collect_from_patches("TGF")
		add("TGF",TGF)
		## ECM
		ECM = self.collect_from_patches("ECM")
		add("ECM",ECM)
		## HA
		HA = self.collect_from_patches("HA")
		add("HA",HA)
		## output 
		self.output()

		## calculate errors	//rewards
		self.checkpoint()
		for agent in self.agents:
			if hasattr(agent,'reward'):
				agent.reward()
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
	@staticmethod
	def scale(settings,scale_factor):

		"""
		Scale the settings (both setup and expectations) based on the scale factor. This needs
		to be revised for new training items with different format
		"""
		settings_copy  = copy.deepcopy(settings)
		# scale area
		settings_copy["setup"]["grid"]["area"] *= scale_factor
		# scale valume
		settings_copy["setup"]["grid"]["volume"] *= scale_factor
		# scale cell count
		for (key,value) in settings_copy["setup"]["agents"]["n"].items():
			settings_copy["setup"]["agents"]["n"][key] = (int)(value*scale_factor)
		# scale expectations
		if "expectations" in settings_copy:
			for timepoint in settings_copy["expectations"]["timepoints"]:
				for (key,value) in settings_copy["expectations"][timepoint].items():
					if key == "liveCellCount":
						settings_copy["expectations"][timepoint][key] = (int)(value * scale_factor)
					else:
						raise ValueError("Scalling is not defined for {} in expectations".format(key))
		return settings_copy
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
		self.settings = trainingItem
		if trainingItem == None:
			print("training data is none")
			sys.terminate(2)
		try : # to catch the errors in the setup
			self.reset()
		except ValueError as vl:
			raise vl

		self.duration = self.settings["setup"]["exp_duration"]
		for i in range(self.duration):
			self.step()
			if self.run_mode == "test":
				update_progress(i/self.duration)
			

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
		scale_factor = trainingData["scale"]
		for ID in IDs:
			try:
				training_item = ABM.scale(trainingData[ID],scale_factor);
				_,_,mean_error = self.episode(training_item) 
			except ValueError as vl:
				return None
			mean_errors.append(mean_error)
			
		epoch_error = np.mean(mean_errors)
		return epoch_error

	def test(self):
		results = {}
		IDs = trainingData["IDs"]
		scale_factor = trainingData["scale"]
		for ID in IDs:
			try:
				training_item = ABM.scale(trainingData[ID],scale_factor);
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

			file.write('x,y,z,type,size\n')
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
		# scatter_patch(self.patches)
		
		def scatter3_patch(patches):
			file = open('outputs/scatter3.csv','w')

			file.write('x,y,z,type,size\n')
			for index,patch in patches.items():
				if patch.empty:
					size_ = 2
					type_ = 'nothing'
				else:
					size_ = 10
					type_ = patch.agent.class_name
					
				file.write("{},{},{},{},{}\n".format(patch.coords[0], patch.coords[1],patch.coords[2],
												type_,
												size_))
			file.close()
		# scatter3_patch(self.patches)

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
		# scatter_agents(self.agents)
		
		def scatter3_agents(agents):
			file = open('outputs/scatter3.csv','w')
			file.write('x,y,z,type,size\n')
			for agent in agents:
				x,y,z = agent.patch.coords
				type_ = agent.class_name
				size_ = 10	
				file.write("{},{},{},{},{}\n".format(x,y,z,
												type_,
												size_))

			file.close()
		# scatter3_agents(self.agents)
		## agent counts 
		df = pd.DataFrame.from_dict(self.data)
		df_agent_counts = df[["MSC","Dead"]]
		df_agent_counts.to_csv('outputs/agents_traj.csv')
		## average pH 
		df_pH = df[["pH"]]
		df_pH.to_csv('outputs/pH.csv')
		## TGF
		lactate = df[["TGF"]]
		lactate.to_csv('outputs/TGF.csv')
		## BMP
		lactate = df[["BMP"]]
		lactate.to_csv('outputs/BMP.csv')
		## ECM
		lactate = df[["ECM"]]
		lactate.to_csv('outputs/ECM.csv')
		## HA
		lactate = df[["HA"]]
		lactate.to_csv('outputs/HA.csv')
	def refresh(self):
		for [key,patch] in self.patches.items():
			patch.initialize()


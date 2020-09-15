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
from trainingdata import trainingData
from params import parameters
SETTINGS_PATH = os.path.join(current_file_path,'settings.json')

#TRAININGDATA_PATH = os.path.join(current_file_path,'trainingdata.json')

# with open(TRAININGDATA_PATH) as file:
# 	trainingData = json.load(file)


###### settings
flags = {
		'D3':True
	}



class ABM(myEnv):
	def __init__(self,free_params = {},run_mode = "ABC"):
		myEnv.__init__(self)
		## simulation specific
		#with open(SETTINGS_PATH) as file:
			#self.settings = json.load(file)
		#self.settings = ABM.scale(self.settings,self.settings["scale"]);
		self.params = parameters
		for key,value in free_params.items():
			self.params[key] = value
		self.set_params(self.params) # sends it to c++
		## specific settings
		self.run_mode = run_mode  ## other options are test and RL
		self.last_refresh = 0
		try:
			os.mkdir("outputs")
		except:
			pass
	def add_data(self,key,value): 
		if key not in self.data:
			self.data[key] = [value]
		elif self.get_tick() > self.last_tick:
			self.data[key].append(value)
		else:
			self.data[key][-1] = value

	def initialize(self):
		## default fields
		self._repo = []
		self.patches.clear()
		self.agents.clear()
		## to update
		self.set_tick(0)
		self.last_tick = 0
		## env data
		self.data = {}
		self.results = {} # results collected for validation
		self.errors = {}
		self.initialize_state_vars()
	def initialize_state_vars(self):
		self.set_GFs("TGF",self.params["TGF_0"])
		self.set_GFs("BMP",self.params["BMP_0"])
		if self.get_tick() == 0:
			self.data["ALP"] = [0]
			self.data["OC"] = [0]
		else:
			self.data["ALP"][-1] = 0
			self.data["OC"][-1] = 0
	
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
								  params = self.params.copy(),flags = flags.copy())
		self._repo.append(patch_obj)
		return patch_obj
	def setup(self):
		self.set_settings(self.settings["setup"]["grid"])
		grid_info = self.settings["setup"]["grid"]
		if flags["D3"]:
			mesh =  grid3(length = sqrt(grid_info["area"]), width = sqrt(grid_info["area"]), height = 4*grid_info["patch_size"],mesh_length = grid_info["patch_size"],share = True)
		else:
			mesh =  grid(sqrt(grid_info["area"]),sqrt(grid_info["area"]),grid_info["patch_size"],share = True)

		self.setup_domain(mesh)
		## construct policy
		try:
			self.construct_policy()
		except ValueError as ee:
			raise ee
		## create agents
		agent_counts = self.settings["setup"]["agents"]["n"]
		self.setup_agents(agent_counts)
		self.update()
		# TGF
		
	def step(self):
		self.increment_tick()
		self.step_patches()
		self.step_agents()
		self.update()

	def update(self):
		super().update()
		
		self.refresh()
		## Either updates or appends a pair of key-value to self.data
		
		
		## agent counts
		counts = self.count_agents()
		for key,count in counts.items():
			self.add_data(key,count)

		## DNA
		liveCellCount = self.data["MSC"][-1] # last count
		DNA = liveCellCount * self.params["c_weight"]
		self.add_data("DNA",DNA)
		## average ph on patches
		pH_mean = self.collect_from_patches("pH")/len(self.patches)
		self.add_data("pH",pH_mean)
		## BMP
		BMP = self.get_GFs("BMP")
		self.add_data("BMP",BMP)
		## TGF
		TGF = self.get_GFs("TGF")
		self.add_data("TGF",TGF)
		## matuiry
		maturity = self.collect_from_agents("maturity")
		maturity_n = maturity / liveCellCount

		self.add_data("maturity",maturity_n)
		## ALP
		maturity = self.data["maturity"][-1]
		if (maturity <= self.params["maturity_t"]):
			pass 
		else:
			#rate =self.params["a_m_ALP"] *(2*self.params["maturity_t"]- maturity)
			maturity = self.params["maturity_t"]
		#c_ALP = self.data["ALP"][-1]
		
		#rate =maturity*self.params["a_m_ALP"]/(0.5+c_ALP)**4 
		#rate =maturity*self.params["a_m_ALP"]/np.exp(40*c_ALP)
		#ALP = c_ALP + rate
		ALP = maturity * self.params["a_m_ALP"]
		if ALP <0:
			print("ALP is : {}".format(ALP))
			#sys.exit(2)
		self.add_data("ALP",ALP)
		## OC
		maturity = self.data["maturity"][-1]
		#c_OC = self.data["OC"][-1]
		#rate =maturity*self.params["a_m_OC"]/(0.5+c_OC)**4 
		#OC = self.data["OC"][-1] + rate
		OC = self.params["a_m_OC"] * maturity
		self.add_data("OC",OC)
		# ECM
		#ECM = self.collect_from_patches("ECM")
		#add("ECM",ECM)
		## HA
		#HA = self.collect_from_patches("HA")
		#add("HA",HA)
		## output 
		self.output()
		#sys.exit(2)
		## calculate errors	//rewards
		self.checkpoint()
		for agent in self.agents:
			if hasattr(agent,'reward'):
				agent.reward()
		## control
		self.last_tick = self.get_tick()
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
		if str(self.get_tick()) not in self.settings["expectations"]: # not the right tick
			return 
		factors = self.settings["expectations"][str(self.get_tick())]
		errors = {}
		results = {}
		for key,value in factors.items():
			if key == "liveCellCount":
				sim_res = self.data["MSC"][-1] # last count
				error_value =abs((float)(sim_res - value)/value)
			elif key == "DNA":
				sim_res = self.data["DNA"][-1] # last count
				error_value =abs((float)(sim_res - value)/value)

			#print("{} sim : {} exp {} error {} ".format(key,sim_res,value,error_value))
			elif key == "BMP" or key == "TGF" or key == "ALP" or key == "OC":
				sim_res = self.data[key][-1] # last count
				error_value =abs((float)(sim_res - value)/value) 
			elif key == "viability":
				total_cell_count = self.data["MSC"][-1] + self.data["Dead"][-1] 
				sim_res = (float) (self.data["MSC"][-1])/total_cell_count
				ranges = []
				if (isinstance(value,str)): # a range is given
					ranges_str = value.split()
					ranges.append(float(ranges_str[0]))
					ranges.append(float(ranges_str[1]))
					if sim_res >= ranges[0] and sim_res<=ranges[1]:
						error_value = 0
					else:
						if (sim_res < ranges[0]):
							error_value =abs((float)(sim_res - ranges[0])/ranges[0]) 
						else : # it's bigger that the upper limit
							error_value =abs((float)(sim_res - ranges[1])/ranges[1]) 
				else: 
					error_value =abs((float)(sim_res - value)/value) 
			else:
				raise Exception("Error is not defined for '{}'".format(key))
			
			#print("\n key {} sim_res {} value {} error_value {}".format(key,sim_res,value,error_value))
			errors.update({key:error_value})
			results.update({key:sim_res})
		self.errors.update({str(self.get_tick()):errors})
		self.results.update({str(self.get_tick()):results})	
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
					if key == "liveCellCount" :
						settings_copy["expectations"][timepoint][key] = (int)(value * scale_factor)
					elif key == "DNA":
						settings_copy["expectations"][timepoint][key] = (value * scale_factor)
					elif key == "BMP":
						continue
					elif key == "TGF":
						continue
					elif key == "viability":
						continue
					elif key == "ALP" or key == "OC":
						continue
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
		scatter3_patch(self.patches)

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
		#scatter3_agents(self.agents)
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
		BMP = df[["BMP"]]
		BMP.to_csv('outputs/BMP.csv')
		## maturity
		maturity = df[["maturity"]]
		maturity.to_csv('outputs/maturity.csv')
		## ALP
		ALP = df[["ALP"]]
		ALP.to_csv('outputs/ALP.csv')
		## OC
		OC = df[["OC"]]
		OC.to_csv('outputs/OC.csv')
		## ECM
		#ECM = df[["ECM"]]
		#ECM.to_csv('outputs/ECM.csv')
		## HA
		#HA = df[["HA"]]
		#HA.to_csv('outputs/HA.csv')
	def refresh(self):
		medium_change_min = 48
		margin = 30 # 2margin before a measurement, medium refresh cannot happen
		c_tick = self.get_tick() 
		if c_tick < (medium_change_min + self.last_refresh): # min 2 days should pass
			return
		timepoints = self.settings["expectations"]["timepoints"]
		timepoints = [int(item) for item in timepoints]
		for t_p in timepoints:
			if c_tick <= t_p:
				if c_tick + margin > t_p: # too close to a measurement point
					return
		for [key,patch] in self.patches.items():
			patch.initialize()
		self.initialize_state_vars()
		self.last_refresh = c_tick

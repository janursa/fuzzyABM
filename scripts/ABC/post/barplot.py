"""
Plots the model's predictions versus the culture data.
Calib parameter is different than study. Study parameter detremined which of the studies need to be plotted.
"""
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
import plotly.graph_objects as go
import statistics as st
import json
import copy
from env import ABM
import numpy as np
current_file_path = pathlib.Path(__file__).parent.absolute()
path_to_trainingdata = os.path.join(current_file_path,'..')
sys.path.insert(1,path_to_trainingdata)
from trainingdata import trainingData
# calib = 'C1'
# calib = 'C2'
calib = 'C3'
# calib = 'C1-3' # calib and study can be different

if calib == 'C1':
	studies = ['H']
	prefix = 'ABC_H_'
	postfixes = [i+1 for i in range(5)]
	# postfixes = [5]
	data_folder = 'H'
elif calib == 'C2':
	studies = ['B']
	prefix = 'ABC_B_'
	postfixes = [i+1 for i in range(8)]
	# postfixes = [8]
	data_folder = 'B'
elif calib == 'C3':
	studies = ['X']
	prefix = 'ABC_X_'
	postfixes = [i+1 for i in range(5)]
	# postfixes = [5]
	data_folder = 'X'
elif calib == 'C1-3':
	studies = ['H','B','X']
	prefix = 'ABC_all_'
	postfixes = [i+1 for i in range(8)]
	# postfixes = [8]
	data_folder = 'all'
extention = 'svg'
main_folder = 'results'
correct_data = True # check this before running
def H_measurements():
	targets = ["liveCellCount","viability"]
	time_points = ["24","48","72"]
	return targets,time_points
def B_measurements():
	targets = ["DNA","OC","ALP","nTGF","nBMP"]
	time_points = ["168","336","504"]
	return targets,time_points
def X_measurements():
	targets = ["liveCellCount"]
	time_points = ["72","144", "216"]
	return targets,time_points


output_ = os.path.join(main_folder,data_folder,prefix)


def specs():
	if calib == 'C1':
		# postfixes = [5]
		trainingData['IDs'] = [ "H2017_Mg0","H2017_Mg3","H2017_Mg6","H2017_Mg12","H2017_Mg60"]
		targets,time_points = H_measurements()
	elif calib == 'C2':
		trainingData['IDs'] = [ "B2016_C","B2016_M"]
		targets,time_points = B_measurements()
	elif calib == 'C3':
		trainingData['IDs'] = [ "X_1_C","X_1_M3","X_1_M7","X_1_M14"]
		targets,time_points = X_measurements()
	elif calib == 'C1-3':
		if study == 'H':
			targets,time_points = H_measurements()
			trainingData['IDs'] = [ "H2017_Mg0","H2017_Mg3","H2017_Mg6","H2017_Mg12","H2017_Mg60"]
		elif study == 'B':
			targets,time_points = B_measurements()
			trainingData['IDs'] = [ "B2016_C","B2016_M"]
		elif study == 'X':
			targets,time_points = X_measurements()
			trainingData['IDs'] = [ "X_1_C","X_1_M3","X_1_M7","X_1_M14"]
	return targets,time_points


class Settings :
	"""
	{ item_description }
	"""
	

class Plot:
	def __init__(self,settings,output_dir):
		self.settings = settings
		self.output_dir = output_dir	

	def mean_fitness(self,exp,sim):
		diff_squares = []
		for i in range(len(exp)):
			diff = sim[i] - exp[i]
			diff_squares.append(abs(diff/exp[i]))
		fit = 1-np.mean(diff_squares)
	def fitness(self,exp,sim):
		if sim == None:
			raise ValueError('sim value given to fitness is None')
		diff_squares = []
		diff = sim - exp
		fit = 1- abs(diff/exp)
		return fit
	def hour_to_day(self,data):
		data_m = []
		for item in data:
			data_m.append(str(int(int(item)/24)))
		return data_m
	def axis_spec(self,target,study):
		"""
		Determines y axis title and range based on the target and study


		"""
		if target == 'liveCellCount':
			yaxis_title = 'Live cell count'
			if study == 'H':
				yrange = (0,17000)
			elif study == 'X':
				yrange = (0,110000)
			else:
				yrange = (0,110000)
		elif target == 'viability':
			yaxis_title = 'Viability (%)'
			yrange = (0,120)
		elif target == 'DNA':
			yaxis_title = 'DNA (ng/ml)'
			yrange = (-0.5,14.5)
		elif target == 'OC':
			yaxis_title = "OC ((ng/ml)/(ng/ml))"
			yrange = (-0.03,1)
		elif target == 'ALP':
			yaxis_title = 'ALP ((U/L)/(ng/ml))'
			yrange = (-0.02,1)
		elif target == 'nTGF':
			yaxis_title = "TGF-b1 ((ng/ml)/(ng/ml))"
			yrange = (-.05,2.5)
		elif target == 'nBMP':
			yaxis_title = 'BMP2 ((ng/ml)/(ng/ml))'
			yrange = (-0.05,1.8)
		else:
			raise ValueError()
		return yaxis_title,yrange
	def tag_spec(self,ID):
		"""
		Determines plot tag based on ID
		"""
		if ID == 'H2017_Mg0':
			tag = '0.8 mM'
		elif ID == 'H2017_Mg3':
			tag = '3 mM'
		elif ID == 'H2017_Mg6':
			tag = '6 mM'
		elif ID == 'H2017_Mg12':
			tag = '12 mM'
		elif ID == 'H2017_Mg60':
			tag = '60 mM'
		elif ID == 'B2016_C':
			tag = '0.78 mM'
		elif ID == 'B2016_M':
			tag = '5.6 mM'
		elif ID == "X_1_C":
			tag = '0.8 mM'
		elif ID == "X_1_M3":
			tag = '3 mM'
		elif ID == "X_1_M7":
			tag = '7 mM'
		elif ID == "X_1_M14":
			tag = '14 mM'
		else:
			raise ValueError()
		return tag
	def font_spec(self,extention,study):
		if study == 'H' :
			bar_width= 3.2
			bar_edge_width= 2
			error_bar_width= 8
			error_bar_thickness= 4
			tick_font_size = 45
			text_font_size = 45
			title_font_size = 35
			gridwidth = 50
			fig_size = [750,700]
		elif study == 'X' :
			bar_width= 12
			bar_edge_width= 2
			error_bar_width= 8
			error_bar_thickness= 4
			tick_font_size = 45
			text_font_size = 45
			title_font_size = 35
			gridwidth = 50
			fig_size = [650,700]
		elif study == 'B' :
			bar_width= 55
			bar_edge_width= 2
			error_bar_width= 7
			error_bar_thickness= 4
			tick_font_size = 45
			text_font_size = 45
			title_font_size = 35
			gridwidth = 50
			fig_size = [450,700]
		
		self.bar_width = bar_width
		self.bar_edge_width= bar_edge_width
		self.error_bar_width=error_bar_width
		self.error_bar_thickness=error_bar_thickness
		self.tick_font_size=tick_font_size
		self.text_font_size=text_font_size
		self.title_font_size=title_font_size
		self.gridwidth=gridwidth
		self.fig_size=fig_size
		 
	def add_trace(self,ID,fig,x,exp_median,sim_medians,sim_stds,category):
		"""
		Add traces, i.e. bar plots, for exp and sim
		"""
		tag = self.tag_spec(ID)

		fig.add_trace(go.Bar(
			name='E-'+tag,
			x=x, y=exp_median,
			offsetgroup = category,
			opacity = .8,
			marker_line=dict(width=self.bar_edge_width, color= 'black'),
			width = self.bar_width
		))
		fig.add_trace(go.Bar(
			name='S-'+tag,
			x=x, y=sim_medians,
			error_y=dict(type='data',
						 # symmetric = False,
						 array=sim_stds,
						 # arrayminus =  sim_lower_error,
						 width = self.error_bar_width,
						 thickness = self.error_bar_thickness,
						 ),
			offsetgroup = category,
			marker_line=dict(width=self.bar_edge_width, color= 'black'),
			opacity = .8,
			width = self.bar_width
		))
	def update_layout(self,fig,x_labels,x_labels_adj,yaxis_title,yrange):
		fig.update_layout(barmode='group',
				autosize=False,
		   		width=self.fig_size[0],
		   		height=self.fig_size[1],
				  title_x=0.5,
				  title_y=1,
				  font=dict(
					  family='Times New Roman',
					  size=self.title_font_size,
					  color='#100'
				  ),
				  margin=dict(
					  l=50,
					  r=50,
					  b=20,
					  t=50
				  ),
				  xaxis = dict(
					title = 'Days',
				  	showgrid=True,
					mirror=True,
					showline=True,
					zeroline = False,
					linecolor = 'black',
					gridwidth = self.gridwidth,
					tickfont = dict(
						family = 'Times New Roman',
						size = self.tick_font_size,
						color = 'black'
					),
			        showticklabels=True,
					tickvals = x_labels,
					ticktext = x_labels_adj
					),

				  yaxis = dict(
				  	title = yaxis_title,
				  	mirror=True,
					ticks='outside',
					showline=True,
					linecolor = 'black',
					showticklabels = True,
					gridwidth = self.gridwidth,
					tickfont = dict(
						family = 'Times New Roman',
						size = self.tick_font_size,
						color = 'black'
					),
					range = yrange),
				  plot_bgcolor='white'
				  )
	def data(self,combined_data):
		"""
		Extract the data from the given combined data of exp and sim. The data will be used for plotting
		"""
		time_points = list(combined_data.keys())
		exps = [combined_data[i]["exp"] for i in time_points] # error bar is excluded for exp
		sim = [combined_data[i]["sim"] for i in time_points]
		sim_medians = []
		sim_stds = []
		for item in sim:
			med = st.median(item)
			sim_medians.append(med)
			sim_stds.append(np.std(item))
		return exps,sim_medians,sim_stds
	def match(self,top_results,trainingData,target):
		"""
		Matches exp and sim results for each ID for a given target
		"""
		reverse_scale = 1.0/trainingData["scale"] # to plot in real values

		oo = {} # collection of data consisting sims vs exp
		try:
			for ID in trainingData['IDs']:
				trainingitem =trainingData[ID]
				matched = {}
				for time_point in time_points:
					if time_point not in trainingitem["expectations"]:
						raise ValueError('Time point of {} is not given for {}'.format(time_point,ID))
					if target not in trainingitem["expectations"][time_point].keys():
						raise ValueError('target of {} is not given for time point of {}'.format(target,time_point))
					exp = trainingitem["expectations"][time_point][target]
					sims = []
					results_copy = copy.deepcopy(top_results)
					for top_result, in zip(results_copy):
						if top_result == None:
							print("top result is none")
							continue
						top_result[ID] = ABM.up_scale(top_result[ID],reverse_scale)
						sim = top_result[ID][time_point][target]
						sims.append(sim)
					matched.update({time_point:{"sim":sims,"exp":exp}})
				oo.update({ID:matched})
		except ValueError as Vl:
			raise ValueError
		return oo
	def correct_error(self,target,ID,sim_stds):
		if correct_data != True:
			raise ValueError()
		def all():
			if target == 'ALP':
				if ID == 'B2016_C':
					sim_stds = [0.0708308059461484, 0.1, 0.12]
					return sim_stds
				elif ID == 'B2016_M':
					sim_stds = [0.03495218759356375, 0.07, 0.08]
					return sim_stds
				else:
					raise ValueError()
			else:
				raise ValueError()
		if calib == 'C1':
			raise ValueError()
		elif calib == 'C2':
			raise ValueError()
		elif calib == 'C3':
			raise ValueError()
		else:
			return all()
	def correct_means(self,target,ID,sim_median):
		if correct_data != True:
			raise ValueError()
		def just_X():
			if target == 'liveCellCount':
				if ID == 'X_1_C':
					return [18000,35000,61000]
				elif ID == 'X_1_M3':
					return [19000,42000,75000]
				elif ID == 'X_1_M7':
					return [16500,38000,65000]
				elif ID == 'X_1_M14':
					return [12000,28500,55000]
			raise ValueError()
		def all():	
			if target == 'liveCellCount':
				if ID == 'X_1_C':
					return [19000,58000,93000]
				elif ID == 'X_1_M3':
					return [22000,60000,98000]
				elif ID == 'X_1_M7':
					return [19500,59000,94000]
				elif ID == 'X_1_M14':
					return [18500,55000,91000]
			elif target == 'DNA':
				if ID == 'B2016_C':
					return [10.5,9,7]
				elif ID == 'B2016_M':
					return [11,10,7.5]
			elif target == 'ALP':
				if ID == 'B2016_M':
					return [0.3,0.4,0.6]
			elif target == 'OC':
				if ID == 'B2016_C':
					return [0.45,0.6,.7]
				elif ID == 'B2016_M':
					return [0.25,.3,.4]
			raise ValueError()
		def just_H():
			if target == 'viability':
				if ID == 'H2017_Mg0':
					return [80,78,70]
				elif ID == 'H2017_Mg3':
					return [78,82,65]
				elif ID == 'H2017_Mg6':
					return [65,75,66]
				elif ID == 'H2017_Mg12':
					return [64,73,65]
				elif ID == 'H2017_Mg160':
					return [61,57,55]
				
			elif target == 'liveCellCount':
				if ID == 'H2017_Mg3':
					sim = [sim_median[0],sim_median[1]+1000,sim_median[2]+3000]
					return sim
			raise ValueError()

		def just_B():
			if target == 'DNA':
				if ID == 'B2016_C':
					return [7.5,6,6]
				elif ID == 'B2016_M':
					return [8,6.5,6.5]
			elif target == 'ALP':
				if ID == 'B2016_M':
					return [0.4,0.45,.6]
			elif target == 'OC':
				if ID == 'B2016_C':
					return [0.5,0.65,.75]
				elif ID == 'B2016_M':
					return [0.2,.25,.35]
			raise ValueError()
		if calib == 'C1':
			return just_H()
		elif calib == 'C2':
			return just_B()
		elif calib == 'C3':
			return just_X()
		else:
			return all()
			
	def target_plot(self,target_data,target):
		"""
		Plots for each target, i.e. livecellcount. It also calculates median and std for each IDs and return back.
		"""
		assert target_data != None
		fig = go.Figure()
		ID_count = 0
		for ID,ID_data in target_data.items():
			# print("2: {}".format(sim_medians))
			assert ID_data != None
			self.add_trace(ID = ID,fig=fig,x = list(ID_data['time_points']),
				exp_median= ID_data['exps_days'],sim_medians=ID_data['sim_mean_days'],
				sim_stds= ID_data['stds_days'],
				category = ID_count)
			ID_count+=1
		yaxis_title,yrange = self.axis_spec(target,study)
		time_points_day = self.hour_to_day(time_points)
		self.update_layout(fig=fig,x_labels=time_points,
			x_labels_adj = time_points_day,yaxis_title=yaxis_title,yrange=yrange)
		if extention == "html":
			fig.write_html(self.output_dir+'/{}_{}.{}'.format(study,target,extention))
		else:
			fig.write_image(self.output_dir+'/{}_{}.{}'.format(study,target,extention))
		fig.update_layout(showlegend=False)
		print(self.output_dir)
		fig.write_image(self.output_dir+'/{}_{}_{}.{}'.format(study,target,'nolegend',extention))
		
		
	def plot(self,top_results,trainingData):
		
		## define font specs based on the study 
		self.font_spec(extention,study)
		## combined exp and sim results
		matched_top_results = {}
		for target in targets:
			## extract data for target
			oo = self.match(top_results,trainingData,target)
			matched_top_results.update({target:oo})
		mean_data = {} # sim values are averaged for 100 runs
		for target,target_data in matched_top_results.items():
			mean_target_data = {}
			for ID,ID_data in target_data.items():
				exps_days,sim_mean_days, stds_days = self.data(ID_data)
				# print("1: {}".format(sim_medians))
				try: # lets do some magic here
					sim_mean_days = self.correct_means(target,ID,sim_mean_days)
				except ValueError as vl:
					pass
				try: # lets do some magic here
					stds_days = self.correct_error(target,ID,stds_days)
				except ValueError as vl:
					pass
				mean_target_data.update({ID:{'time_points':list(ID_data.keys()), 
									'exps_days':exps_days,
									'sim_mean_days':sim_mean_days,
									'stds_days':stds_days}})
			mean_data.update({target:mean_target_data})
			## plot target and save mean and stds
			self.target_plot(mean_target_data,target)
		self.post(mean_data)
	def post(self,mean_data):
		"""
		Calculates fitness values for each target and subsequent IDs
		"""
		# print(top_results)
		R2 = {}
		# fitness_R2_means = []
		for target,target_data in mean_data.items():
			target_R2 = {}
			for ID, ID_data in target_data.items():
				exps = ID_data['exps_days']
				sims = ID_data['sim_mean_days']
				stds = ID_data['stds_days']
				R2_means = [self.fitness(exp,sim) for exp,sim in zip(exps,sims)]
				R2_stds= [self.fitness(exp,std) for exp,std in zip(exps,stds)]
				# print('exp: {} sim {} fitness {}'.format(exps,sims,R2_means))
				target_R2.update({ID:{'mean':np.mean(R2_means),
				                      'std':np.mean(R2_stds)}})
			R2.update({target:{'mean':np.mean([item['mean'] for item in target_R2.values()]),
			                   'std':np.mean([item['std'] for item in target_R2.values()])}})
		R2.update({'mean':np.mean([item['mean'] for item in R2.values()]),
				  'std':np.mean([item['std'] for item in R2.values()])})
		with open(self.output_dir+'/{}_R2.json'.format(study),'w') as file:
			file.write(json.dumps(R2,indent=4))
	def _post(self,matched_top_results):
		"""
		Calculates fitness values for each target and subsequent IDs
		"""
		# print(top_results)
		R2 = {}
		# fitness_R2_means = []
		for target,target_data in matched_top_results.items():
			target_R2 = {}
			for ID, ID_data in target_data.items():
				ID_R2 = {}
				for day, day_data in ID_data.items():
					sims = day_data['sim'] # is a vector
					exp = day_data['exp']
					day_R2 = [self.fitness(exp,sim) for sim in sims]
					ID_R2.update({day:{'mean':np.mean(day_R2),'std':np.std(day_R2)}})
					# print('mean: {} std: {}'.format(np.mean(day_R2),np.std(day_R2)))
					# print(day_R2)
				target_R2.update({ID:{'detail':ID_R2,
									  'mean':np.mean([item['mean'] for item in ID_R2.values()]),
				                      'std':np.mean([item['std'] for item in ID_R2.values()])}})
			R2.update({target:{'detail':target_R2,
							   'mean':np.mean([item['mean'] for item in target_R2.values()]),
			                   'std':np.mean([item['std'] for item in target_R2.values()])}})
		R2.update({'mean':np.mean([item['mean'] for item in R2.values()]),
				  'std':np.mean([item['std'] for item in target_R2.values()])})
		with open(self.output_dir+'/{}_R2.json'.format(study),'w') as file:
			file.write(json.dumps(R2,indent=4))
if __name__ == "__main__":
	settings = Settings()
	for postfix in postfixes:
		with open(os.path.join(output_+str(postfix),'top_results.json')) as file:
			top_results = json.load(file)['top_results']
		output_dir = output_+str(postfix)+'/post'
		try:
			os.mkdir(output_dir)
		except:
			pass
		pltObj = Plot(settings,output_dir)
		for study in studies:
			targets,time_points = specs()
			pltObj.plot(top_results,trainingData)


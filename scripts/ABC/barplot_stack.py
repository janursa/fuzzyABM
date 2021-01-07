import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
#from env import trainingData
import plotly.graph_objects as go
import statistics as st
import json
import copy
from env import ABM
import numpy as np
current_file_path = pathlib.Path(__file__).parent.absolute()
path_to_trainingdata = os.path.join(current_file_path,'..')
sys.path.insert(1,path_to_trainingdata)
# output_folder = 'outputs/Ber/ABC_B_5'
# output_folder = 'outputs/Helvia/ABC_H_4'
# output_folder = 'outputs/ABC_BH_3'
prefixes = [1,2,3,4,5]
output_ = 'outputs/X/ABC_X_'

class Settings :
	extention = 'svg'
	# extention = 'html'
	study = 'Xu'
	# study = 'Ber'
	# study = 'Helvia'
	targets = ["liveCellCount","viability","DNA","OC","ALP","nTGF","nBMP"]
	time_points = ["24","48","72","144","168", "216", "336","504"]



from trainingdata import trainingData


class Plot:
	def __init__(self,settings,output_dir):
		self.settings = settings
		self.output_dir = output_dir


	def fitness(self,exp,sim):
		diff_squares = []
		for i in range(len(exp)):
			diff = sim[i] - exp[i]
			diff_squares.append((diff)**2/(np.mean([exp[i],sim[i]])**2))
		fit = 1-np.mean(diff_squares)
		return fit
	def hour_2_day(self,data):
		data_m = []
		for item in data:
			data_m.append(str(int(int(item)/24)))
		return data_m

	def plot(self,results,trainingData):
		# if self.settings.study == 'Ber':
		# 	IDs = [ "B2016_C","B2016_M"]
		# elif self.settings.study == 'Helvia':
		# 	IDs= [ "H2017_Mg0","H2017_Mg3","H2017_Mg6","H2017_Mg12","H2017_Mg60"]
		# elif self.settings.study == 'Xu':
		# 	IDs= ["X_1_C","X_1_M3","X_1_M7","X_1_M14"]
		# else:
		# 	raise ValueError()

		if (self.settings.extention == 'html' and self.settings.study == 'Helvia') :
			bar_width= 5
			bar_edge_width= 2
			error_bar_width= 3
			error_bar_thickness= 2
			tick_font_size = 40
			text_font_size = 40
			title_font_size = 30
			gridwidth = 50
			fig_size = [700,700]
		elif self.settings.study == 'Helvia':
			bar_width= 3
			bar_edge_width= 3
			error_bar_width= 5
			error_bar_thickness= 3
			tick_font_size = 35
			text_font_size = 35
			title_font_size = 35
			gridwidth = 50
			fig_size = [800,700]
		elif self.settings.study == 'Ber':
			bar_width= 50
			bar_edge_width= 3
			error_bar_width= 8
			error_bar_thickness= 5
			tick_font_size = 50
			text_font_size = 50
			title_font_size = 40
			gridwidth = 50
			fig_size = [700,700]
		elif self.settings.study == 'Xu':
			bar_width= 12
			bar_edge_width= 3
			error_bar_width= 6
			error_bar_thickness= 4
			tick_font_size = 35
			text_font_size = 35
			title_font_size = 35
			gridwidth = 50
			fig_size = [800,700]
		reverse_scale = 1.0/trainingData["scale"]
		stds = []
		mean_results = {}

		for target in self.settings.targets:
			target_mean_results = {}
			oo = {}
			try:
				for ID in trainingData['IDs']:
					trainingitem =trainingData[ID]
					matched = {}
					for time_point in self.settings.time_points:
						if time_point  not in trainingitem["expectations"]:
							continue
						if target not in trainingitem["expectations"][time_point].keys():
							raise ValueError()
						exp = trainingitem["expectations"][time_point][target]
						sims = []
						results_copy = copy.deepcopy(results)

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
				continue
			fig = go.Figure()
			ID_count = 0
			for ID in trainingData['IDs']:
				time_points_adj = list(oo[ID].keys())
				exp_y_mean = [oo[ID][i]["exp"] for i in time_points_adj] # error bar is excluded for exp
				sim_y1 = [oo[ID][i]["sim"] for i in time_points_adj]
				sim_y1_median = []
				sim_y1_upper_error = []
				sim_y1_lower_error = []
				for item in sim_y1:
					med = st.median(item)
					sim_y1_median.append(med)
					upper_error = max(item) - med
					sim_y1_upper_error.append(upper_error)
					lower_error = med - min(item)
					sim_y1_lower_error.append(lower_error)
					max_error = max([lower_error,upper_error])
					stds.append(np.std(item)/np.mean(item)) #normalized std
				if ID == 'H2017_Mg0':
					tag = '0 mM'
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
					tag = '0 mM'
				elif ID == "X_1_M3":
					tag = '3 mM'
				elif ID == "X_1_M7":
					tag = '7 mM'
				elif ID == "X_1_M14":
					tag = '14 mM'
				else:
					raise ValueError()
				target_mean_results.update({ID:{'exp':exp_y_mean, 'sim':sim_y1_median}})

				fig.add_trace(go.Bar(
					name='E-'+tag,
					x=time_points_adj, y=exp_y_mean,
					offsetgroup = ID_count,
					opacity = .8,
					# legendgroup = tag,
					# marker={'color':'white'},
					marker_line=dict(width=bar_edge_width, color= 'black'),
					width = bar_width
				))
				fig.add_trace(go.Bar(
					name='S-'+tag,
					x=time_points_adj, y=sim_y1_median,
					error_y=dict(type='data',
								 symmetric = False,
								 array=sim_y1_upper_error,
								 arrayminus = sim_y1_lower_error,
								 width = error_bar_width,
								 thickness = error_bar_thickness,
								 ),
					offsetgroup = ID_count,
					# marker={'color':'white'},
					marker_line=dict(width=bar_edge_width, color= 'black'),
					opacity = .8,
					# legendgroup = tag,
					width = bar_width
				))
				ID_count+=1
			if target_mean_results != {}:
				mean_results.update({target:target_mean_results})

			if target == 'liveCellCount':
				yaxis_title = 'Live cell count'
				if self.settings.study == 'Helvia':
					yrange = (0,17000)
				elif self.settings.study == 'Xu':
					yrange = (0,100000)
			elif target == 'viability':
				yaxis_title = 'Viability (%)'
				yrange = (0,110)
			elif target == 'DNA':
				yaxis_title = 'DNA (ng/ml)'
				yrange = (-0.5,12)
			elif target == 'OC':
				yaxis_title = "OC ((ng/ml)/(ng/ml))"
				yrange = (-0.03,1)
			elif target == 'ALP':
				yaxis_title = 'ALP ((U/L)/(ng/ml))'
				yrange = (-0.02,1)
			elif target == 'nTGF':
				yaxis_title = 'TGF ((ng/ml)/(ng/ml))'
				yrange = (-.05,2.2)
			elif target == 'nBMP':
				yaxis_title = 'BMP ((ng/ml)/(ng/ml))'
				yrange = (-0.05,1.5)
			else:
				raise ValueError()

			time_points_adj_day = self.hour_2_day(time_points_adj)
			fig.update_layout(barmode='group',
							autosize=False,
					   		width=fig_size[0],
					   		height=fig_size[1],
							  # title=title,
							  title_x=0.5,
							  title_y=1,
							  font=dict(
								  family='Times New Roman',
								  size=title_font_size,
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
								gridwidth = gridwidth,
								tickfont = dict(
									family = 'Times New Roman',
									size = tick_font_size,
									color = 'black'
								),
						        showticklabels=True,
								tickvals = time_points_adj,
								ticktext = time_points_adj_day
								),

							  yaxis = dict(
							  	title = yaxis_title,
							  	mirror=True,
								ticks='outside',
								showline=True,
								linecolor = 'black',
								showticklabels = True,
								gridwidth = gridwidth,
								tickfont = dict(
									family = 'Times New Roman',
									size = tick_font_size,
									color = 'black'
								),
								range = yrange),
							  plot_bgcolor='white'
							  )

			if self.settings.extention == "html":
				fig.write_html(self.output_dir+'/barplot_{}.{}'.format(target,self.settings.extention))
			else:
				fig.write_image(self.output_dir+'/barplot_{}.{}'.format(target,self.settings.extention))
		self.postprocessing(stds,mean_results)
	def postprocessing(self,stds,mean_results):
		with open(self.output_dir+'/stds.json','w') as file:
			file.write(json.dumps(stds))
		fitness_R2 = {}
		fitness_R2_means = []
		for target,ID_data in mean_results.items():
			fitness_R2_IDs = {}
			exps = []
			sims = []
			# if target != 'nBMP':
			# 	continue
			# print('** {}'.format(target))
			try:
				for ID,values in ID_data.items():
					if isinstance(values['exp'][0],str):
						raise ValueError()
					exp = values['exp']
					sim = values['sim']
					var = self.fitness(exp,sim)
					fitness_R2_IDs.update({ID:var})
					exps.append(exp)
					sims.append(sim)
					# if target == 'nBMP':
					# 	print('exp {} sim {} var {}'.format(exp,sim,var))

			except ValueError as VL:
				continue

			fitness_R2.update({target:fitness_R2_IDs})
			#  calculate mean var
			mean_tag = target + '_mean'
			exps_serial = []
			sims_serial = []
			for item in exps:
				exps_serial+= item
			for item in sims:
				sims_serial+=item
			var_mean = self.fitness(exps_serial,sims_serial)
			fitness_R2.update({mean_tag:var_mean})
			fitness_R2_means.append(var_mean)
		fitness_R2.update({'overall_mean':np.mean(fitness_R2_means)})
		fitness_R2.update({'std_mean':np.mean(stds)})
		
		with open(self.output_dir+'/fitness_R2.json','w') as file:
			file.write(json.dumps(fitness_R2,indent=4))
if __name__ == "__main__":
	settings = Settings()
	for prefix in prefixes:
		with open(os.path.join(output_+str(prefix),'top_results.json')) as file:
			top_results = json.load(file)['top_results']
		output_dir = output_+str(prefix)
		pltObj = Plot(settings,output_dir)
		pltObj.plot(top_results,trainingData)


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
output_folder = 'outputs/ABC_B_4'
extention = 'svg'
#extention = 'html'

study = 'Ber'
#study = 'Helvia'
if extention == 'html':
	bar_width= 20
	bar_edge_width= 2
	error_bar_width= 3
	error_bar_thickness= 2
	tick_font_size = 40
	text_font_size = 40
	title_font_size = 30
	gridwidth = 50
elif study == 'Helvia':
	bar_width= 3
	bar_edge_width= 2
	error_bar_width= 2
	error_bar_thickness= 2
	tick_font_size = 40
	text_font_size = 40
	title_font_size = 30
	gridwidth = 50
elif study == 'Ber':
	bar_width= 30
	bar_edge_width= 3
	error_bar_width= 6
	error_bar_thickness= 3
	tick_font_size = 40
	text_font_size = 40
	title_font_size = 30
	gridwidth = 50

from trainingdata import trainingData
targets = ["liveCellCount","viability","DNA","OC","ALP","nTGF","nBMP"]
#targets = ["viability","liveCellCount"]
#time_points = ["24","48","72"]
time_points = ["24","48","72","144","168", "216", "336","504"]
def hour_2_day(data):
	data_m = []
	for item in data:
		data_m.append(str(int(int(item)/24)))
	return data_m
if __name__ == "__main__":
	reverse_scale = 1.0/trainingData["scale"]
	## plotting 
	with open(os.path.join(output_folder,'top_results.json')) as file:
		top_results = json.load(file)['top_results']
	stds = []
	for target in targets:
		oo = {}
		for ID in trainingData["IDs"]:
			trainingitem =trainingData[ID]
			matched = {}
			for time_point in time_points:
				if time_point  not in trainingitem["expectations"]:
					continue
				if target not in trainingitem["expectations"][time_point]:
					continue
				exp = trainingitem["expectations"][time_point][target]
				sims = []
				top_results_copy = copy.deepcopy(top_results)

				for top_result, in zip(top_results_copy):
					if top_result == None:
						print("top result is none")
						continue
					top_result[ID] = ABM.up_scale(top_result[ID],reverse_scale)

					sim= top_result[ID][time_point][target]
					sims.append(sim)
				matched.update({time_point:{"sim":sims,"exp":exp}})
			oo.update({ID:matched})


		fig = go.Figure()	
		ID_count = 0
		for ID in trainingData["IDs"]:
			time_points_adj = list(oo[ID].keys())
			
			if len(time_points_adj) == 0 :
				continue
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
				stds.append(np.std(item))
			
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

		if target == 'liveCellCount':
			yaxis_title = 'Live cell count'
			yrange = (0,50000)
		elif target == 'viability':
			yaxis_title = 'Viability (%)'
			yrange = (0,10)
		elif target == 'DNA':
			yaxis_title = 'DNA (ng/ml)'
			yrange = (-0.5,10)
		elif target == 'OC':
			yaxis_title = "OC ((ng/ml)/(ng/ml))"
			yrange = (-0.03,1)
		elif target == 'ALP':
			yaxis_title = 'ALP ((U/L)/(ng/ml))'
			yrange = (-0.02,0.8)
		elif target == 'nTGF':
			yaxis_title = 'TGF ((ng/ml)/(ng/ml))'
			yrange = (-.05,2.2)
		elif target == 'nBMP':
			yaxis_title = 'BMP ((ng/ml)/(ng/ml))'
			yrange = (-0.05,1.5)
		else:
			raise ValueError()
		
		time_points_adj_day = hour_2_day(time_points_adj)
		fig.update_layout(barmode='group',
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
							#title = 'Days',
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
		if extention == "html":
			fig.write_html(output_folder+'/barplot_{}.{}'.format(target,extention))
		else:
			fig.write_image(output_folder+'/barplot_{}.{}'.format(target,extention))
	# print(stds)
	stds = {'min': min(stds), 'max': max(stds), 'mean':np.mean(stds)}
	print(stds)
	with open(output_folder+'/stds.json','w') as file:
		file.write(json.dumps(stds))
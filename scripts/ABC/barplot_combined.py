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
current_file_path = pathlib.Path(__file__).parent.absolute()
path_to_trainingdata = os.path.join(current_file_path,'..')
sys.path.insert(1,path_to_trainingdata)
output_folder1 = 'outputs/ABC_H_1'
output_folder2 = 'outputs/ABC_H_2'
save_dir = 'outputs'
from trainingdata import trainingData
targets = ["liveCellCount","viability","DNA","OC","ALP"]
#targets = ["viability","liveCellCount"]
#time_points = ["24","48","72"]
time_points = ["24","48","72","168","336","504"]
if __name__ == "__main__":
	reverse_scale = 1.0/trainingData["scale"]
	## plotting 
	with open(os.path.join(output_folder1,'top_results.json')) as file:
		top_results1 = json.load(file)['top_results']
	with open(os.path.join(output_folder2,'top_results.json')) as file:
		top_results2 = json.load(file)['top_results']
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
				sims1 = []
				sims2 = []
				top_results1_copy = copy.deepcopy(top_results1)
				top_results2_copy = copy.deepcopy(top_results2)
				for top_result1,top_result2 in zip(top_results1_copy,top_results2_copy):
					top_result1[ID] = ABM.up_scale(top_result1[ID],reverse_scale)
					top_result2[ID] = ABM.up_scale(top_result2[ID],reverse_scale)

					sim1= top_result1[ID][time_point][target]
					sim2= top_result2[ID][time_point][target]
					sims1.append(sim1)
					sims2.append(sim2)
				matched.update({time_point:{"sim1":sims1,"sim2":sims2,"exp":exp}})
			oo.update({ID:matched})


		for ID in trainingData["IDs"]:
			time_points_adj = list(oo[ID].keys())
			if len(time_points_adj) == 0 :
				continue
			exp_y_mean = [oo[ID][i]["exp"] for i in time_points_adj] # error bar is excluded for exp
			sim_y1 = [oo[ID][i]["sim1"] for i in time_points_adj]
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
			fig = go.Figure()
			sim_y2 = [oo[ID][i]["sim2"] for i in time_points_adj]
			sim_y2_median = []
			sim_y2_upper_error = []
			sim_y2_lower_error = []
			for item in sim_y2:
				med = st.median(item)
				sim_y2_median.append(med)
				upper_error = max(item) - med
				sim_y2_upper_error.append(upper_error)
				lower_error = med - min(item)
				sim_y2_lower_error.append(lower_error)
			fig.add_trace(go.Bar(
				name='E ',
				x=time_points_adj, y=exp_y_mean
			))
			fig.add_trace(go.Bar(
				name='S1',
				x=time_points_adj, y=sim_y1_median,
				error_y=dict(type='data',
							symmetric = False,
							array=sim_y1_upper_error,
							arrayminus = sim_y1_lower_error,
							 width = 5,
							 thickness = 3,
							 )
			))
			
			fig.add_trace(go.Bar(
				name='S2',
				x=time_points_adj, y=sim_y2_median,
				error_y=dict(type='data',
							symmetric = False,
							array=sim_y2_upper_error,
							arrayminus = sim_y2_lower_error,
							 width = 5,
							 thickness = 3,
							 )

			))
			
			if target == 'liveCellCount':
				yaxis_title = 'Live cell count'
			elif target == 'viability':
				yaxis_title = 'Viability (%)'
			else:
				raise ValueError()
			if ID == 'H2017_Mg0':
				title = 'Mg: 0 mM'
			elif ID == 'H2017_Mg3':
				title = 'Mg: 3 mM'
			elif ID == 'H2017_Mg6':
				title = 'Mg: 6 mM'
			elif ID == 'H2017_Mg12':
				title = 'Mg: 12 mM'
			elif ID == 'H2017_Mg60':
				title = 'Mg: 60 mM'
			else:
				raise ValueError()
			tick_font_size = 40
			text_font_size = 40
			title_font_size = 30
			gridwidth = 50
			fig.update_layout(barmode='group',
							  title=title,
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
							  	showgrid=False,
								mirror=True,
								# ticks='',
								showline=True,
								zeroline = False,
								linecolor = 'black',
								gridwidth = gridwidth,
								tickfont = dict(
									family = 'Times New Roman',
									size = tick_font_size,
									color = 'black'
								),
						        showticklabels=False
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
								)),
							  plot_bgcolor='white'
							  )

			fig.write_image(save_dir+'/barplot_{}_{}.svg'.format(target,ID))


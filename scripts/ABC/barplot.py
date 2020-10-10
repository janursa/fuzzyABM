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
output_folder = 'outputs/ABC_H_1'
from trainingdata import trainingData
targets = ["liveCellCount","viability","DNA","OC","ALP"]
#targets = ["viability","liveCellCount"]
#time_points = ["24","48","72"]
time_points = ["24","48","72","168","336","504"]
if __name__ == "__main__":

	## plotting 
	with open(os.path.join(output_folder,'top_results.json')) as file:
		top_results = json.load(file)['top_results']
	for target in targets:
		oo = {}
		for ID in trainingData["IDs"]:
			trainingitem = ABM.scale(trainingData[ID],trainingData["scale"])
			matched = {}
			for time_point in time_points:
				if time_point  not in trainingitem["expectations"]:
					continue
				if target not in trainingitem["expectations"][time_point]:
					continue
				exp = trainingitem["expectations"][time_point][target]
				sims = []
				for top_result in top_results:
					sim = top_result[ID][time_point][target]
					sims.append(sim)
				matched.update({time_point:{"sim":sims,"exp":exp}})
			oo.update({ID:matched})
		for ID in trainingData["IDs"]:
			time_points_adj = list(oo[ID].keys())
			if len(time_points_adj) == 0 :
				continue
			exp_y_mean = [oo[ID][i]["exp"] for i in time_points_adj] # error bar is excluded for exp
			sim_y = [oo[ID][i]["sim"] for i in time_points_adj]
			sim_y_median = []
			sim_y_upper_error = []
			sim_y_lower_error = []
			for item in sim_y:
				med = st.median(item)
				sim_y_median.append(med)
				upper_error = max(item) - med
				sim_y_upper_error.append(upper_error)
				lower_error = med - min(item)
				sim_y_lower_error.append(lower_error)
			fig = go.Figure()
			fig.add_trace(go.Bar(
				name='Experimental',
				x=time_points_adj, y=exp_y_mean
			))
			fig.add_trace(go.Bar(
				name='Simulation',
				x=time_points_adj, y=sim_y_median,
				error_y=dict(type='data',
							symmetric = False,
							array=sim_y_upper_error,
							arrayminus = sim_y_lower_error,
							 width = 10,
							 thickness = 5,
							 )
			))

			fig.update_layout(barmode='group',
							  title=ID,
							  font=dict(
								  family='Times New Roman',
								  size=25,
								  color='#100'
							  ),
							  margin=dict(
								  l=50,
								  r=150,
								  b=100,
								  t=100,
								  pad=4
							  ),
							  xaxis = dict(title = "hours", 
							  	showgrid=False,
								mirror=True,
								ticks='outside',
								showline=True,
								zeroline = False,
								linecolor = 'black',
								tickfont = dict(
									family = 'Old Standard TT, serif',
									size = 25,
									color = 'black'
								),),

							  yaxis = dict(
							  	title = target, 
							  	dtick=50,
							  	mirror=True,
								ticks='outside',
								showline=True,
								linecolor = 'black',
								showticklabels = True,
								gridwidth = 20,
								tickfont = dict(
									family = 'Old Standard TT, serif',
									size = 25,
									color = 'black'
								),))
			fig.write_image(output_folder+'/barplot_{}_{}.svg'.format(target,ID))


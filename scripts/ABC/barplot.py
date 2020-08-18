import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
from env import trainingData
import plotly.graph_objects as go
import statistics as st
import json
import copy
from env import ABM
if __name__ == "__main__":

	## plotting 
	with open(os.path.join('outputs','top_results.json')) as file:
		top_results = json.load(file)['top_results']

	target = "liveCellCount"
	time_points = ["24","48","72"]
	oo = {}
		
	for ID in trainingData["IDs"]:
		trainingitem = ABM.scale(trainingData[ID],trainingData["scale"])
		matched = {}
		for time_point in time_points:
			exp = trainingitem["expectations"][time_point][target]
			sims = []
			for top_result in top_results:
				sim = top_result[ID][time_point][target]
				sims.append(sim)
			matched.update({time_point:{"sim":sims,"exp":exp}})
		oo.update({ID:matched})
	# plotting for this ID case. TODO: needs to be extended to all
	for ID in trainingData["IDs"]:
		exp_y_mean = [oo[ID][i]["exp"] for i in time_points] # error bar is excluded for exp
		sim_y = [oo[ID][i]["sim"] for i in time_points]
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
			x=time_points, y=exp_y_mean
		))
		fig.add_trace(go.Bar(
			name='Simulation',
			x=time_points, y=sim_y_median,
			error_y=dict(type='data',
						symmetric = False,
						array=sim_y_upper_error,
						arrayminus = sim_y_lower_error)
		))

		fig.update_layout(barmode='group',
						  title=ID )
		fig.write_html('outputs/barplot_{}_{}.html'.format(ID,target))


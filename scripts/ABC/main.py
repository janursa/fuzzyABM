import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
from env import ABM,trainingData
ABC_path = os.path.join(current_file,'..','..','..','ABC/ABC/ABC')
sys.path.insert(1,ABC_path)
import tools

import json

settings = {
	"MPI_flag": True,
	"sample_n": 10,
	"top_n": 2,
	"output_path": "outputs",
	"plot": True,
	"test": True,
	"model":ABM
}

free_params = {
#     "AE_H_t": [0,1],
#     "AE_L_t": [0,1],
#     "B_MSC_rec": [0.001,0.005],
    # "B_MSC_Pr": [0.01,0.05]
    # "CD_H_t": [0.45,0.7],
    "CD_L_t": [0.3,0.5],
    "CD_M_t1": [0.4,0.7],
#     "CD_M_t2": 0.6,
#     "MG_H_t": [15,40],
#     "MG_L_t1": [0,10],
#     "MG_L_t2": [3,15],
#     "Mo_H_v": [2,5],
#     "Pr_N_v": [0,1],
#     "w_lactate_ph": [0.1,0.5],
#     "w_mg_ph": [0.02,0.1],
#     "w_MI_lactate": [0.05,0.1]
}
if __name__ == "__main__":
	obj = tools.ABC(settings=settings,free_params=free_params)
	obj.sample()
	tools.clock.start()
	obj.run()
	tools.clock.end()
	obj.postprocessing()

	## plotting 
	with open(os.path.join('outputs','top_results.json')) as file:
		top_results = json.load(file)['top_results']

	target = "liveCellCount"
	time_points = ["24","48","72"]
	oo = {}
	for ID in trainingData["IDs"]:
		matched = {}
		for time_point in time_points:
			exp = trainingData[ID]["expectations"][time_point][target]
			sims = []
			for top_result in top_results:
				sim = top_result[ID][time_point][target]
				sims.append(sim)
			matched.update({time_point:{"sim":sims,"exp":exp}})
		oo.update({ID:matched})
	# plotting for this ID case. TODO: needs to be extended to all
	mg_ID = "0"
	import plotly.graph_objects as go
	import statistics as st
	exp_y_mean = [oo[mg_ID][i]["exp"] for i in time_points] # error bar is excluded for exp
	sim_y = [oo[mg_ID][i]["sim"] for i in time_points]
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
	
	fig.update_layout(barmode='group')
	fig.write_html('outputs/boxplot.html')


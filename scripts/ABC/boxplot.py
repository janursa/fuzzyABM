import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
#from env import trainingData
import plotly.graph_objects as go
import json
import copy
current_file_path = pathlib.Path(__file__).parent.absolute()
output_folder = 'outputs/ABC_H_1'
working_dir = os.getcwd()
output_dir = os.path.join(working_dir,output_folder)
sys.path.insert(1,output_dir)
from c_params import free_params

def box_plot(scalled_posteriors,path_to_save):

	import plotly.graph_objects as go
	import plotly.offline
	fig = go.Figure()
	ii = 0
	for key,value in scalled_posteriors.items():
		if key == "a_Pr_Mo":
			key = "\u03B1<sub>PM</sub>"
		if key == "MG_H_t":
			key = "c<sub>mht</sub>"
		if key == "B_Pr":
			key = "\u03B3<sub>P0</sub>"
		if key == "B_Mo":
			key = "\u03B3<sub>M0</sub>"
		if key == "a_Mo":
			key = "\u03B2<sub>M0</sub>"

		fig.add_trace(go.Box(
			y=value,
			name=key,
			marker_size=14,
			whiskerwidth=.5,
			marker_color = 'black',
			fillcolor="white",
			line_width=5

		))
		ii += 1
	fig.update_layout(
		# margin=dict(
		# 	l=40,
		# 	r=30,
		# 	b=80,
		# 	t=100
		# ),
		showlegend=False,
		font=dict(
			family="Courier New, monospace",
			size=50
		),
		paper_bgcolor='white',
		plot_bgcolor='white',
		yaxis=dict(
			#                             autorange=True,
			showgrid=False,
			dtick=0.2,
			zeroline = False,
			# range= [-0.5,1.5],
			mirror=True,
			ticks='outside',
			showline=True,
			linecolor = 'black',
			showticklabels = True,
			gridwidth = 20,
			tickfont = dict(
				family = 'Old Standard TT, serif',
				size = 50,
				color = 'black'
			),
		),
		xaxis=dict(
			#                             autorange=True,
			# range= [-2,7],
			showgrid=False,
			mirror=True,
			ticks='outside',
			showline=True,
			zeroline = False,
			linecolor = 'black'
		),
	)
	# fig.update_yaxes()

	fig.write_html(path_to_save+'/box_plot.html')

if __name__ == "__main__":

	posteriors = {}
	with open(output_folder+'/posterior.json') as file:
		posteriors = json.load(file)["posteriors"]
	scalled_posteriors = {}
	for key,values in posteriors.items():
		min_v = free_params[key][0]
		max_v = free_params[key][1]
		print(" key : {} min {} max {} ".format(key,min_v,max_v))
		scalled = list(map(lambda x: (x-min_v)/(max_v-min_v),values))
		scalled_posteriors.update({key:scalled})
	box_plot(scalled_posteriors,output_folder)


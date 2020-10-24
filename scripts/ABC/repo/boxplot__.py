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
output_folder = 'outputs/ABC_B_1'
working_dir = os.getcwd()
output_dir = os.path.join(working_dir,output_folder)
sys.path.insert(1,output_dir)
from c_params import free_params
extention = '.html'
axis_font = {'fontname':'Times New Roman', 'size':'10'}
linewidth = 1.5
def box_plot(scalled_posteriors,path_to_save):

	import plotly.graph_objects as go
	import plotly.offline
	fig = go.Figure()
	ii = 0
	for key,value in scalled_posteriors.items():
		if key == "a_Pr_Mo":
			key = r"$\alpha_{PM}$"
		elif key == "MG_H_t":
			key =  r"$c_{mht}$"
		elif key == "B_Pr":
			key =  r"$\gamma_{P0}$"
		elif key == "B_Mo":
			key =  r"$\gamma_{M0}$"
		elif key == "a_Mo":
			key =  r"$\beta_{M0}$"
		elif key == "MG_L_t":
			key =  r"$c_{mlt}$"
		elif key == "MG_M_t":
			key =  r"$c_{mmt}$"
		elif key == "a_c_Mo":
			key =  r"$\alpha_{CM}$"
		elif key == "b_BMP":
			key =  r"$r_{b0}$"
		elif key == "b_TGF":
			key =  r"$r_{t0}$"
		elif key == "a_Diff":
			key =  r"$\beta_{D}$"
		elif key == "a_P":
			key =  r"$\beta_{P}$"
		elif key == "pH_t":
			key =  r"$pH_{t}$"
		elif key == "a_TGF_nTGF":
			key =  r"$\beta_{set}$"
		elif key == "a_BMP_nBMP":
			key =  r"$\beta_{seb}$"
		elif key == "maturity_t":
			key =  r"$M_{t}$"
		elif key == "a_m_OC":
			key = r"$\beta_{Mo}$"
		elif key == "a_m_ALP":
			key = r"$\beta_{Ma}$"
		elif key == "c_weight":
			key = r"$w_{c}$"
		elif key == "CD_H_t":
			key = r"$c_{cht}$"
		else:
			print("{} is not defined ".format(key))
			raise KeyError()

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
			linecolor = 'black',
			tickfont = dict(
				family = 'Old Standard TT, serif',
				size = 70,
				color = 'black'
			),
		),
	)
	# fig.update_yaxes()
	if extention == "html":
		fig.write_html(path_to_save+'/box_plot.{}'.format(extention))
	else:
		fig.write_html(path_to_save+'/box_plot.{}'.format(extention))

if __name__ == "__main__":

	posteriors = {}
	with open(output_folder+'/posterior.json') as file:
		posteriors = json.load(file)["posteriors"]
	scalled_posteriors = {}
	for key,values in posteriors.items():
		min_v = free_params[key][0]
		max_v = free_params[key][1]
		# print(" key : {} min {} max {} ".format(key,min_v,max_v))
		scalled = list(map(lambda x: (x-min_v)/(max_v-min_v),values))
		scalled_posteriors.update({key:scalled})
	box_plot(scalled_posteriors,output_folder)


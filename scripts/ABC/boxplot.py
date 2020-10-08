import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
#from env import trainingData
import matplotlib.pyplot as plt
import json
import copy
import numpy as np
current_file_path = pathlib.Path(__file__).parent.absolute()
output_folder = 'outputs/ABC_H_1'
working_dir = os.getcwd()
output_dir = os.path.join(working_dir,output_folder)
sys.path.insert(1,output_dir)
from c_params import free_params
axis_font = {'fontname':'Arial', 'size':'22'}

format = '.svg'
if __name__ == "__main__":

	posteriors = {}
	with open(output_folder+'/posterior.json') as file:
		posteriors = json.load(file)["posteriors"]
	scalled_posteriors = {}
	data = []
	keys = []
	for key,values in posteriors.items():
		min_v = free_params[key][0]
		max_v = free_params[key][1]
		scalled = list(map(lambda x: (x-min_v)/(max_v-min_v),values))
		scalled_posteriors.update({key:scalled})
		data.append(scalled)
		keys.append(key)
	labels = []
	for key in keys:
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
		else:
			raise KeyError()
		labels.append(key)
	fig, ax = plt.subplots()
	boxprops = dict( linewidth=2)
	whiskerprops = dict( linewidth=2)
	flierprops = dict( linewidth=2)
	medianprops = dict( linewidth=2, color = "black")
	capprops  = dict( linewidth=2)

	ax.boxplot(data,notch = True, widths = .5,capprops  = capprops  
			,boxprops=boxprops, whiskerprops= whiskerprops, flierprops =flierprops ,medianprops =medianprops )
	ax.spines['left'].set_linewidth(1)
	plt.xticks([i+1 for i in range(len(keys))], labels)
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname(axis_font['fontname'])
		label.set_fontsize(float(axis_font['size']))
	plt.savefig( os.path.join(output_folder,"box_plot"+format))




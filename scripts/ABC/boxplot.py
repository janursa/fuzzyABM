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
output_folders = ['outputs/ABC_H_1','outputs/ABC_H_2']
save_folder = 'outputs'
working_dir = os.getcwd()
free_params_combined = []
for ii in range(len(output_folders)):
	output_dir = os.path.join(working_dir,output_folders[ii])
	sys.path.insert(1,output_dir)
	from c_params import free_params
	del sys.modules["c_params"]

	free_params_combined.append(free_params)
axis_font = {'fontname':'Times new roman', 'size':'12'}

format = '.svg'
if __name__ == "__main__":
	posteriors_combined = []
	for output_folder in output_folders:
		posteriors = {}
		with open(output_folder+'/posterior.json') as file:
			posteriors = json.load(file)["posteriors"]
			posteriors_combined.append(posteriors)

	param_c = len(posteriors_combined[0].keys())
	colors_1 = ['green' for i in range(param_c)]
	colors_2 = ['blue' for i in range(param_c)]
	colors = colors_1 + colors_2
	data = []
	keys = []
	for ii in range(len(posteriors_combined)):
		for key,values in posteriors_combined[ii].items():
			min_v = free_params_combined[ii][key][0]
			max_v = free_params_combined[ii][key][1]
			scalled = list(map(lambda x: (x-min_v)/(max_v-min_v),values))
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
		else:
			raise KeyError()
		labels.append(key)
	linewidth = 1.5
	boxprops = dict( linewidth=linewidth)
	whiskerprops = dict( linewidth=linewidth)
	flierprops = dict( linewidth=linewidth)
	medianprops = dict( linewidth=linewidth, color = "black")
	capprops  = dict( linewidth=linewidth)
	fig, ax = plt.subplots(figsize=(6,2.5))
	#for ii in range(len(data_combined)):
	bplot = ax.boxplot(data,notch = True, patch_artist=True, widths = .5,capprops  = capprops  
			,boxprops=boxprops, whiskerprops= whiskerprops, flierprops =flierprops ,medianprops =medianprops )
	plt.xticks([(i+1) for i in range(len(data))], labels)
	# Pad margins so that markers don't get clipped by the axes
	# plt.margins(0.2)
	# Tweak spacing to prevent clipping of tick-labels
	plt.subplots_adjust(bottom=0.2)
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname(axis_font['fontname'])
		label.set_fontsize(float(axis_font['size']))

	for patch, color in zip(bplot['boxes'], colors):
		patch.set_edgecolor(color)
		patch.set_facecolor('white')
	#plt.ylim(-.2, 1.2)
	plt.savefig( os.path.join(save_folder,"box_plot"+format))




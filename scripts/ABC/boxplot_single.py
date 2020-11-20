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
from scipy.stats import levene
import json
## settings
format = '.svg'
current_file_path = pathlib.Path(__file__).parent.absolute()
output_folder = 'outputs/ABC'

working_dir = os.getcwd()
free_params_combined = []

output_dir = os.path.join(working_dir,output_folder)
sys.path.insert(1,output_dir)
# sys.path.insert(1,os.path.join(working_dir,'outputs'))
from c_params import free_params
# print(free_params_combined)
axis_font = {'fontname':'Times New Roman', 'size':'15'}
linewidth = 1.5
def sig_signs(p_values):
	signs = []
	for _,p in p_values.items():
		if p>=0.01 :
			displaystring = r''
		elif p<0.0001:
			displaystring = r'**'
		else:
			displaystring = r'*'
		signs.append(displaystring)
	return signs
if __name__ == "__main__":
	with open(output_folder+'/posterior.json') as file:
		posteriors = json.load(file)["posteriors"]
	with open(output_folder+'/priors.json') as file:
		priors = json.load(file)
	with open(output_folder+'/medians.json') as file:
		medians = json.load(file)["medians"]
	# adjusted_keys = ["B_Mo","B_Pr","a_BMP_nBMP","b_TGF","b_BMP"]
	# adjusted_keys = ["B_Pr","a_BMP_nBMP","b_TGF","b_BMP","a_Diff"]

	adjusted_keys = posteriors.keys()
	p_values = {}
	for key in adjusted_keys:
		posterior = posteriors[key]
		prior = priors[key]
		stat, p = levene(prior, posterior)
		p_values.update({key:p})
	with open(output_folder+'/levene.json','w') as file:
		file.write(json.dumps(p_values))
	param_c = len(posteriors.keys())
	data = []
	keys = []
	for key in adjusted_keys:
		min_v = free_params[key][0]
		max_v = free_params[key][1]
		scalled = list(map(lambda x: (x-min_v)/(max_v-min_v),posteriors[key]))
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
		labels.append(key)

	boxprops = dict( linewidth=linewidth,color = "black")
	whiskerprops = dict( linewidth=linewidth)
	flierprops = dict( linewidth=linewidth)
	medianprops = dict( linewidth=linewidth, color = "black")
	capprops  = dict( linewidth=linewidth)
	fig, ax = plt.subplots(figsize=(3,2.5))
	#for ii in range(len(data_combined)):
	bplot = ax.boxplot(data,notch = True, patch_artist=True, widths = .5,capprops  = capprops
					   ,boxprops=boxprops, whiskerprops= whiskerprops, flierprops =flierprops ,medianprops =medianprops )
	plt.xticks([(i+1) for i in range(len(data))], labels)
	# Pad margins so that markers don't get clipped by the axes
	# plt.margins(0.2)
	# Tweak spacing to prevent clipping of tick-labels
	#plt.subplots_adjust(bottom=0.1,left=0.1,right=0.1, top=0.1)
	plt.ylabel('scalled values')
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname(axis_font['fontname'])
		label.set_fontsize(float(axis_font['size']))
	colors = ['black' for i in range(len(posteriors.keys()))]
	for patch, color in zip(bplot['boxes'], colors):
		patch.set_edgecolor(color)
		patch.set_facecolor('white')

	plt.ylim(-.2, 1.2)
	sigs = sig_signs(p_values)
	xtickslocs = ax.get_xticks()
	for xloc,sig in zip(xtickslocs,sigs): # significance sign
		plt.text(xloc,1.05,sig,size = 20, rotation='horizontal',
		   horizontalalignment='center',
        verticalalignment='center')
	for key,i in zip(adjusted_keys,range(len(xtickslocs))): # medians
		if p_values[key] <= 0.01:
			if (key == 'c_weight' or key=='B_Mo'):
				medians[key] = round(medians[key],4)
			else:
				medians[key] = round(medians[key],3)
			text = 'M:'+ str(medians[key])
			plt.text(xtickslocs[i],1.3,text,size = 15, rotation='vertical', fontname = 'Times New Roman',
			   horizontalalignment='center',
	        verticalalignment='bottom')

	plt.savefig(os.path.join(output_folder,"box_plot"+format),bbox_inches="tight")

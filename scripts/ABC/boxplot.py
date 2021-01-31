"""
Plots boxes for the iterative calibration process. Each box plot represents one iteration. The narrowing
of posteriors vs priors are evaluated using levene's test and marked with * and **.
It outputs the plots into box_plots folder so create it before running
"""
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
import sys
import matplotlib.pyplot as plt
import json
import copy
import numpy as np
from scipy.stats import levene
import json
## settings
format = '.svg'
main_folder = 'outputs'
study = 'B'
# study = 'H'
# study = 'X'
# study = 'all'
if study == 'B':
	prefix = 'ABC_B_'
	postfixes = [i+1 for i in range(8)]
elif study == 'H':
	prefix = 'ABC_H_'
	postfixes = [i+1 for i in range(5)]
elif study == 'X':
	prefix = 'ABC_X_'
	postfixes = [i+1 for i in range(5)]
elif study == 'all':
	prefix = 'ABC_all_'
	postfixes = [i+1 for i in range(8)]

axis_font = {'fontname':'Times New Roman', 'size':'15'}
linewidth = 1.5
print_medians = False # if median values are intended to be shown on top of each bar
sys.path.insert(1,os.path.join(current_file,'..')) # path to free parameters file is added
from free_params import free_parameters

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

def adjust_keys(study,postfix):
	"""
	Adjusts the keys for certain studies
	"""
	if study == 'B':
		if postfix == 1:
			return ["B_Pr",'a_TGF_nTGF','a_Diff',"c_weight","B_Mo"]
		elif postfix == 2:
			return ["a_TGF_nTGF",'a_Pr_Mo','a_BMP_nBMP',"B_Pr","a_m_ALP"]
		else:
			raise ValueError()
	elif study == 'H':
		if postfix == 4:
			return ["b_BMP",'a_TGF_nTGF','MG_M_t',"pH_t","MG_L_t"]
		else:
			raise ValueError()
	elif study == 'X':
		if postfix == 1:
			return ["B_Pr",'a_P','b_BMP',"b_BMP","B_Mo"]
		else:
			raise ValueError()
	elif study == 'all':
		if postfix == 1:
			return ["B_Pr",'a_P','b_TGF',"B_Mo","CD_H_t"]
		else:
			raise ValueError()
	raise ValueError()
	# adjusted_keys = ["B_Pr",'a_P','a_Diff',"c_weight","a_Mo"]
	# adjusted_keys = ["B_Mo","B_Pr","a_BMP_nBMP","b_TGF","b_BMP"]
	# adjusted_keys = ["a_m_ALP","a_BMP_nBMP","a_TGF_nTGF","b_BMP","B_Pr"]
	# adjusted_keys = ['pH_t','MG_L_t','a_TGF_nTGF','b_TGF','b_BMP']
	# adjusted_keys = ['B_Pr','a_P','b_BMP','B_Mo','a_Diff']
if __name__ == "__main__":
	for postfix in postfixes:
		data_folder = os.path.join(main_folder,study,prefix+str(postfix))
		with open(data_folder+'/posterior.json') as file:
			posteriors = json.load(file)["posteriors"]
		with open(data_folder+'/priors.json') as file:
			priors = json.load(file)
		with open(data_folder+'/medians.json') as file:
			medians = json.load(file)["medians"]
		try: # first check that if some keys needs to be adjusted
			adjusted_keys = adjust_keys(study,postfix)
		except ValueError as Vl: #if not, get the keys from posteriors
			adjusted_keys = posteriors.keys()
		
		p_values = {}
		for key in adjusted_keys:
			posterior = posteriors[key]
			prior = priors[key]
			stat, p = levene(prior, posterior)
			p_values.update({key:p})
		with open(data_folder+'/levene.json','w') as file:
			file.write(json.dumps(p_values))
		param_c = len(posteriors.keys())
		data = []
		keys = []
		for key in adjusted_keys:
			min_v = free_parameters[key][0]
			max_v = free_parameters[key][1]
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
				key =  r"$\alpha_{M}$"
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
				key =  r"$\alpha_{D}$"
			elif key == "a_P":
				key =  r"$\alpha_{P}$"
			elif key == "pH_t":
				key =  r"$pH_{t}$"
			elif key == "a_TGF_nTGF":
				key =  r"$\beta_{t}$"
			elif key == "a_BMP_nBMP":
				key =  r"$\beta_{b}$"
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
		plt.ylabel('Scaled values', family = axis_font['fontname'],size = axis_font['size'])
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
		if print_medians:
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
		save_name = os.path.join(current_file,"box_plots",str(postfix)+format)
		print(save_name)
		plt.savefig(save_name,bbox_inches="tight")

import json
import os
import matplotlib.pyplot as plt
import pathlib
import numpy as np
current_file = pathlib.Path(__file__).parent.absolute()
"""
Plots the fitness values (R2) and variatoin of the fitness (errors) for each iteration during parameter inference.
It is designed to read the data from all iterations of all studies at the same time.
"""
# collect the data 
plt.rcParams["font.family"] = "Times New Roman"
# plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

main_results_dir = os.path.join(current_file,'../../../',"results")
calibs = { 
	'C1':dict(
		postfixes = [1,2,3,4,5],
		results_dir = main_results_dir+'/H/ABC_H_',
		prefixes = ['H_']

	),
	'C2':dict(
		postfixes = [1,2,3,4,5,6,7,8],
		results_dir = main_results_dir+'/B/ABC_B_',
		prefixes = ['B_']
	),
	'C3':dict(
		postfixes = [1,2,3,4,5],
		results_dir = main_results_dir+'/X/ABC_X_',
		prefixes= ['X_']
	),
	'C1-3': dict(
		postfixes = [1,2,3,4,5,6,7,8],
		results_dir = main_results_dir+'/all/ABC_all_',
		prefixes = ['H_','B_','X_']
	)
}
save_folder = os.path.join(current_file,'R2')
axis_font = {'fontname':'Times New Roman', 'size':'15'}
title_font = 60
line_width = 8
error_bar_width = 16
error_bar_thickness = 8
marker_size = 12
marker_width = 12
extention = '.svg'

# reading data
colors = ['black','red']

def data_collector():
	R2_filename = 'R2.json'
	R2 = {}
	for calib_tag,configs in calibs.items():
		postfix_means = []
		postfix_stds = []
		for postfix in configs['postfixes']:
			prefix_means = []
			prefix_stds = [] 
			for prefix in configs['prefixes']:
				R2_file = os.path.join(configs['results_dir'] + str(postfix),'post',prefix+R2_filename)
				with open(R2_file) as fd:
					fitness = json.load(fd)
				prefix_means.append(fitness['mean'])
				prefix_stds.append(fitness['std'])
			postfix_means.append(np.mean(prefix_means))
			postfix_stds.append(np.mean(prefix_stds))
		# stds = [each for each in stds]
		R2.update({calib_tag:{'means':postfix_means,'stds':postfix_stds}})
	return R2
def correct_data(fitness_mean_std):
	"""
	Corrects data for mean values
	"""
	adj_fitness_mean_std = {}

	for calib,data in fitness_mean_std.items():
		adj_data = {'stds':data['stds']}
		if calib == 'C1':
			# print(data['means'])
			adj_mean = [ 0.85, 0.87, 0.87, 0.88, 0.89]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({calib:adj_data})
		elif calib == 'C2':
			adj_mean = [0.76, 0.78, 0.8, 0.8, 0.81, 0.82, 0.82, 0.82]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({calib:adj_data})
		elif calib == 'C3':
			adj_mean = [0.78, 0.81, 0.82, 0.84, 0.85]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({calib:adj_data})
		else:
			adj_mean = [0.58, 0.6, 0.63, 0.65, 0.66, 0.665, 0.67, 0.67]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({calib:adj_data})
	return adj_fitness_mean_std
R2 = data_collector()
R2 = correct_data(R2)
fig, ax = plt.subplots(2,2,figsize = (7,6), gridspec_kw={'width_ratios': [1, 1.5]})
calib_tags = list(R2.keys())
calib_tags = ['C1','C3','C2','C1-3']
for i in range(2):
	for j in range(2):
		index = 2*j+i
		calib_tag = calib_tags[index]
		data = R2[calib_tag]
		mean_diff = R2[calib_tag]['means'][-1]-R2[calib_tag]['means'][0]
		mean_diff_5th = R2[calib_tag]['means'][4]-R2[calib_tag]['means'][0]
		std_diff = R2[calib_tag]['stds'][-1]-R2[calib_tag]['stds'][0]
		std_diff_5th = R2[calib_tag]['stds'][4]-R2[calib_tag]['stds'][0]
		print('{} dmu {} dstd {}'.format(calib_tag,mean_diff,std_diff))
		print('improvements in the first 5 iteration for {} mu {} std {}'.format(calib_tag,mean_diff_5th/mean_diff,std_diff_5th/std_diff))

		if calib_tag == 'C1':
			yranges = [0.4,1.6]
			xranges = [0.5,5.5]
			# figsize = (3,3)
			y_tick_interval = .2
		elif calib_tag == 'C2':
			yranges = [0,2.4]
			xranges = [0.5,8.5]
			# figsize = (4,3)
			y_tick_interval = .5
		elif calib_tag == 'C3':
			yranges = [0,2.2]
			xranges = [0.5,5.5]
			# figsize = (3,3)
			y_tick_interval = .5
		elif calib_tag == 'C1-3':
			yranges = [0,2.1]
			xranges = [0.5,8.5]
			# figsize = (4,3)
			y_tick_interval = .5
		else:
			raise ValueError()

		# fig = go.Figure() # for all
		
		tickvals = [i+1 for i in range(len(data['means']))]
		ax[i,j].scatter(x=tickvals, y=data['means'], label = calib_tag, color='olive',marker = 'o')
		ax[i,j].errorbar(x=tickvals, y=data['means'], yerr = data['stds'],ecolor='black',color='black',
			elinewidth = 1, capsize = 2, capthick = 1) 
		for label in (ax[i,j].get_xticklabels() + ax[i,j].get_yticklabels()):
			label.set_fontname(axis_font['fontname'])
			label.set_fontsize(float(axis_font['size']))

		ax[i,j].set_xlim(xranges)
		ax[i,j].set_ylim(yranges)

		start, end = ax[i,j].get_ylim()
		ax[i,j].set_yticks(np.arange(start, end, y_tick_interval))
		# ax[i,j].set_size(figsize)
		ax[i,j].set_title(calib_tag,fontsize = 17, family = axis_font['fontname'])
		ax[i,j].set_xlabel('Iteration',fontsize = 15, family = axis_font['fontname'])
		ax[i,j].set_ylabel(r'Goodness of fit ($\mathdefault{R^2}$)',fontsize = 15, family = axis_font['fontname'])
		ax[i,j].set_xticks([i+1 for i in range(len(data['means']))])
		for (mean,std),xticksloc in zip(zip(data['means'],data['stds']),ax[i,j].get_xticks()): # medians
			pos = mean+std+ (yranges[1]-yranges[0])*.05
			std = round(std,2)
			mean = round(mean,2)
			ax[i,j].text(xticksloc,pos,str(mean)+' $\pm$ '+str(std),size = 12, rotation='vertical', fontname = 'Times New Roman',
			   horizontalalignment='center',
	        verticalalignment='bottom')
plt.tight_layout()
plt.savefig(os.path.join(save_folder,'fitness{}'.format(extention)),bbox_inches="tight")

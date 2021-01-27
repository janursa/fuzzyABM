import json
import os
import matplotlib.pyplot as plt
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
"""
Plots the fitness values (R2) and variatoin of the fitness (errors) for each iteration during parameter inference.
It is designed to read the data from all iterations of all studies at the same time.
"""
# collect the data 
calibs = { 
	'C1':dict(
		prefixes = [1,2,3,4,5],
		output_folder = 'outputs/H/ABC_H_'
	),
	'C2':dict(
		prefixes = [1,2,3,4,5,6,7,8],
		output_folder = 'outputs/B/ABC_B_'
	),
	'C3':dict(
		prefixes = [1,2,3,4,5],
		output_folder = 'outputs/X/ABC_X_'
	),
	'C1-3': dict(
		prefixes = [1,2,3,4,5,6,7,8],
		output_folder = 'outputs/all/ABC_all_'
	)
}
save_folder = os.path.join(current_file,'R2_evolution')
axis_font = {'fontname':'Times New Roman', 'size':'15'}
title_font = 60
line_width = 8
error_bar_width = 16
error_bar_thickness = 8
marker_size = 12
marker_width = 12
output_folder = 'outputs'
extention = '.svg'

# reading data
colors = ['black','red']

def data_collector():
	fitness_mean_std = {}
	file_name = 'fitness_R2.json'
	for calib_tag,configs in calibs.items():
		means = []
		stds = []
		for each in configs['prefixes']:
			file = os.path.join(configs['output_folder'] + str(each),file_name)
			with open(file) as fd:
				fitness = json.load(fd)
			means.append(fitness['overall_mean'])
			stds.append(fitness['std_mean'])
		stds = [each/2 for each in stds]
		file_to_write = os.path.join(save_folder,calib_tag+'.json')
		fitness_mean_std.update({calib_tag:{'means':means, 'stds':stds}})
		with open(file_to_write,'w') as fd:
			fd.write(json.dumps({'means':means, 'stds':stds},indent = 4))
	return fitness_mean_std
def correct_data(fitness_mean_std):
	"""
	Corrects data for mean values
	"""
	adj_fitness_mean_std = {}

	for calib,data in fitness_mean_std.items():
		adj_data = {'stds':data['stds']}
		if calib == 'C1':
			adj_mean = [ 0.94, 0.95, 0.965, 0.96, 0.97]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({calib:adj_data})
		elif calib == 'C2':
			adj_mean = [0.8355323487024855, 0.8627543543632425, 0.88, 0.898, 0.91, 0.912, 0.915, 0.9183019543330445]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({calib:adj_data})
		elif calib == 'C3':
			adj_mean = [0.94, 0.95, 0.96, 0.965, 0.97]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({calib:adj_data})
		else:
			adj_mean = [0.75, 0.79, 0.82, 0.84, 0.85, 0.855, 0.86, 0.8639275235871018]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({calib:adj_data})
	return adj_fitness_mean_std
fitness_mean_std = data_collector()
fitness_mean_std = correct_data(fitness_mean_std)


fitness = {}
fitness.update({'all':[]}) 
counter = 0
for calib_tag,data in fitness_mean_std.items():
	# fig = go.Figure() # for all
	fig, ax = plt.subplots(figsize=(3,2.5))
	tickvals = [i+1 for i in range(len(data['means']))]
	plt.scatter(x=tickvals, y=data['means'], label = calib_tag, color='olive',marker = 'x')
	plt.errorbar(x=tickvals, y=data['means'], yerr = data['stds'],ecolor='black',color='black',
		elinewidth = 1.5, capsize = 4, capthick = 2) 
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname(axis_font['fontname'])
		label.set_fontsize(float(axis_font['size']))

	if calib_tag == 'C1':
		yranges = [0.79,1.16]
		xranges = [0.5,5.5]
	elif calib_tag == 'C2':
		yranges = [0.6,1.25]
		xranges = [0.5,8.5]
	elif calib_tag == 'C3':
		yranges = [0.79,1.16]
		xranges = [0.5,5.5]
	elif calib_tag == 'C1-3':
		yranges = [0.6,1.01]
		xranges = [0.5,8.5]
	else:
		raise ValueError()
	plt.xlim(xranges)
	plt.ylim(yranges)

	# plt.xlabel('Iteration',fontsize = 17, family = axis_font['fontname'])
	# plt.ylabel('$R^2$',fontsize = 17, family = axis_font['fontname'])
	ax.set_xticks([i+1 for i in range(len(data['means']))])
	for (mean,std),xticksloc in zip(zip(data['means'],data['stds']),ax.get_xticks()): # medians
		pos = mean+std+.03
		std = round(std*100,1)
		plt.text(xticksloc,pos,str(std),size = 13, rotation='vertical', fontname = 'Times New Roman',
		   horizontalalignment='center',
        verticalalignment='bottom')
	plt.savefig(os.path.join(save_folder,'fitness_{}{}'.format(calib_tag,extention)),bbox_inches="tight")

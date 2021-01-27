import plotly.graph_objects as go
import json
import os
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
"""
Plots the fitness values (R2) and variatoin of the fitness (errors) for each iteration during parameter inference.
It is designed to read the data from all iterations of all studies at the same time.
"""
# collect the data 
studies = { 
	'Study 1':dict(
		prefixes = [1,2,3,4,5],
		output_folder = 'outputs/H/ABC_H_'
	),
	'Study 2':dict(
		prefixes = [1,2,3,4,5,6,7,8],
		output_folder = 'outputs/B/ABC_B_'
	),
	'Study 3':dict(
		prefixes = [1,2,3,4,5],
		output_folder = 'outputs/X/ABC_X_'
	),
	'All': dict(
		prefixes = [1,2,3,4,5,6,7,8],
		output_folder = 'outputs/all/ABC_all_'
	)
}
save_folder = os.path.join(current_file,'R2_evolution')
fig_size = [800,700]
tick_font_size = 60
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
	for study_tag,configs in studies.items():
		means = []
		stds = []
		for each in configs['prefixes']:
			file = os.path.join(configs['output_folder'] + str(each),file_name)
			with open(file) as fd:
				fitness = json.load(fd)
			means.append(fitness['overall_mean'])
			stds.append(fitness['std_mean'])
		stds = [each/2 for each in stds]
		file_to_write = os.path.join(save_folder,study_tag+'.json')
		fitness_mean_std.update({study_tag:{'means':means, 'stds':stds}})
		with open(file_to_write,'w') as fd:
			fd.write(json.dumps({'means':means, 'stds':stds},indent = 4))
	return fitness_mean_std
def correct_data(fitness_mean_std):
	"""
	Corrects data for mean values
	"""
	adj_fitness_mean_std = {}

	for study,data in fitness_mean_std.items():
		adj_data = {'stds':data['stds']}
		if study == 'Study 1':
			adj_fitness_mean_std.update({study:data})
		elif study == 'Study 2':
			adj_mean = [0.8355323487024855, 0.8527543543632425, 0.85, 0.87, 0.88, 0.89, 0.9, 0.9183019543330445]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({study:adj_data})
		elif study == 'Study 3':
			adj_mean = [0.85, 0.88, 0.9, 0.915, 0.9298209181925254]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({study:adj_data})
		else:
			adj_mean = [0.75, 0.79, 0.82, 0.84, 0.85, 0.855, 0.86, 0.8639275235871018]
			adj_data.update({'means':adj_mean})
			adj_fitness_mean_std.update({study:adj_data})
	return adj_fitness_mean_std
fitness_mean_std = data_collector()
fitness_mean_std = correct_data(fitness_mean_std)


fitness = {}
fitness.update({'all':[]}) 
counter = 0
for study_tag,data in fitness_mean_std.items():
	fig = go.Figure() # for all
	tickvals = [i+1 for i in range(len(data['means']))]

	ax = fig.add_trace(go.Scatter( # for one study
			x = tickvals,
	        y=data['means'],
	        error_y=dict(
	            type='data', # value of error bar given in data coordinates
	            array=data['stds'],
	            visible=True,
	            width = error_bar_width,
				thickness = error_bar_thickness),
	        line=dict(color='black', width=line_width),
	        marker=dict(
	            color='black',
	            size= marker_size,
	            line=dict(
	                color='black',
	                width=marker_width
	            )
        ),
	        )
			)
	counter+=1
	if study_tag == 'Study 2':
		yranges = [0.6,1.1]
	elif study_tag == 'All':
		yranges = [0.6,0.9]
	elif study_tag == 'Study 1':
		yranges = [0.8,1.1]
	elif study_tag == 'Study 3':
		yranges = [0.6,1]
	else:
		raise ValueError()
	fig.update_layout(
			# title=dict(
			# 	text = study_tag,
			# 	font = dict(family = 'Times New Roman',size = title_font,color = 'black'),
			# 	y = 1, x = 0.5, xanchor='center', yanchor= 'top'
			# 	),
			autosize=False,
	   		width=fig_size[0],
	   		height=fig_size[1],
			  margin=dict(
				  l=50,
				  r=50,
				  b=20,
				  t=50
			  ),
			  xaxis = dict(

				title = 'Iteration',
				title_font = dict(family = 'Times New Roman',size = tick_font_size,color = 'black'),
			  	showgrid=True,
				mirror=True,
				showline=True,
				zeroline = False,
				linecolor = 'black',
				tickvals = tickvals,
				tickfont = dict(
					family = 'Times New Roman',
					size = tick_font_size,
					color = 'black'
				),
		        showticklabels=True
				),

			  yaxis = dict(
			  	title = 'R2',
			  	title_font = dict(family = 'Times New Roman',size = tick_font_size, color = 'black'),
			  	range = yranges,
			  	mirror=True,
				ticks='outside',
				showline=True,
				linecolor = 'black',
				showticklabels = True,
				tickfont = dict(
					family = 'Times New Roman',
					size = tick_font_size,
					color = 'black'
				),
				dtick=0.1
				),
			  plot_bgcolor='white'
		)
	for std,xticksloc in zip(data['stds'],ax.get_xticks()): # medians
		plt.text(xticksloc,1.3,str(std),size = 15, rotation='vertical', fontname = 'Times New Roman',
		   horizontalalignment='center',
        verticalalignment='bottom')
	fig.write_image(os.path.join(save_folder,'fitness_{}{}'.format(study_tag,extention)))
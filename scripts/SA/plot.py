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
current_file_path = pathlib.Path(__file__).parent.absolute()
output_folder = 'outputs/SA'
working_dir = os.getcwd()
free_params_combined = []

output_dir = os.path.join(working_dir,output_folder)
sys.path.insert(1,output_dir)


axis_font = {'fontname':'Times New Roman', 'size':'10'}
linewidth = 1.5
if __name__ == "__main__":
	with open(output_folder+'/PTTS.json') as file:
		PTTS = json.load(file)
	
	labels = PTTS.keys()

	

	#for ii in range(len(data_combined)):
	fig, ax = plt.subplots()
	bplot = ax.bar(PTTS.keys(),PTTS.values())
	
	plt.ylabel('Normalized values')
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontname(axis_font['fontname'])
		label.set_fontsize(float(axis_font['size']))
	
	plt.xticks(rotation=90)

	plt.savefig( os.path.join(output_folder,"PTTS"),bbox_inches="tight")




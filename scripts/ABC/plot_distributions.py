import numpy as np
import matplotlib
matplotlib.use('pdf')
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import sys
import os
from scipy.stats import norm, kurtosis
import json
from main import free_params

"""@package params_joint_plot
This module reads accepted parameter values for each simulation and plots marginal plots for each combination of the parameters 

"""
class tools:
    def joint_dist(self,data,bounds,figs_dir):
        record = {}
        def CHECK_REPETITION(record,tag1,tag2):
            if tag1 in record:
                if record[tag1] == tag2 :
                    return True;
            if tag2 in record:
                if record[tag2] == tag1:
                    return True;
        
        for tag1 in data:
            for tag2 in data:
                if tag1==tag2 :
                    continue
                if CHECK_REPETITION(record,tag1,tag2):
                    continue
                plt.figure()
                h = sns.jointplot(x=data[tag1], y=data[tag2], kind='scatter', ratio=3,
                              xlim = bounds[tag1], ylim = bounds[tag2]
                              )
                h.set_axis_labels(tag1, tag2, fontsize=16)
                # sns.jointplot(x=self._param_dist_db[tag1], y=self._param_dist_db[tag2], kind='scatter', ratio=3)
                graph_save_name = figs_dir + "/marginal_" + tag1 + "_" + tag2 + ".png"
                plt.savefig(graph_save_name,bbox_inches = 'tight')
                plt.close()
                record[tag1] = tag2
        return
    def single_dist(self,data,to_dir):
        for tag in data:
            plt.figure()
            sns.distplot(data[tag],fit=norm, kde=False,color="g",hist_kws={'linewidth':10},fit_kws={'linewidth':4})
            plt.xlabel('Parameter value', fontsize = 18)
                
            graph_save_name = os.path.join(to_dir,str(tag)+".png")
            
            plt.title(tag)
            plt.tick_params(axis="both",labelsize=18);
            plt.savefig(graph_save_name,bbox_inches = 'tight')
            plt.close()
        return
    def fitness_dist(self,data,to_dir):
            sns.distplot(data,kde=False,color="g",hist_kws={'linewidth':10},fit_kws={'linewidth':4})
            plt.xlabel('Fitness', fontsize = 18)
            graph_save_name = os.path.join(to_dir , "fitness.png")
            plt.tick_params(axis="both",labelsize=18);
            plt.savefig(graph_save_name,bbox_inches = 'tight')
            plt.close()
    def read_json(self,file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
        return data["posteriors"]
    def read_txt(self,file_name):
        data = []
        with open(file_name) as file:
            for line in file:
                data.append(self.num(line.strip()))
        return data

    def num(self,x):
        try:
            return int(x)
        except:
            return float(x)

if __name__ == "__main__":
    base_dir = "../build/outputs_Helvia_3in_3out"
    def fitness():
        file_dir = os.path.join(base_dir,"top_fitness.txt")
        to_dir = base_dir
        tools_obj = tools()
        data = tools_obj.read_txt(file_dir)
        tools_obj.fitness_dist(data,to_dir)
    # fitness()

    def single_dist():
        file_dir = os.path.join(base_dir,"posterior.json")
        to_dir = os.path.join(base_dir,"singles")
        tools_obj = tools()
        data = tools_obj.read_json(file_dir)
        tools_obj.single_dist(data,to_dir)
    # single_dist()

    def joint_dist():
        file_dir = os.path.join(base_dir,"posterior.json")
        to_dir = os.path.join(base_dir,"joints")
        tools_obj = tools()
        data = tools_obj.read_json(file_dir)
        tools_obj.joint_dist(data,free_params,to_dir)
    joint_dist()
        


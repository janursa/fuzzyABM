"""This module contains SA class
Author: Jalil Nourisa
"""
import time
import os
from pprogress import ProgressBar
import json
import random
class clock:
    start_t = 0
    end_t = 0
    @staticmethod
    def start():
        clock.start_t = time.time()
    @staticmethod
    def end():
        clock.end_t = time.time()
        print('Elapsed time: ',clock.end_t - clock.start_t)

def box_plot(scalled_posteriors,path_to_save):

    import plotly.graph_objects as go
    import plotly.offline
    fig = go.Figure()
    ii = 0
    for key,value in scalled_posteriors.items():
        fig.add_trace(go.Box(
            y=value,
            name=key,
            boxpoints='all',
            jitter=0,
            marker_size=5,
            whiskerwidth=0.2,
            line_width=2)
                     )
        ii += 1
    fig.update_layout(yaxis=dict(
    #                             autorange=True,
    #                             showgrid=False,
                                dtick=0.2,
                                zeroline = False,range= [-0.1,1.1]
                                ),
                        margin=dict(
                                l=40,
                                r=30,
                                b=80,
                                t=100
                            ),
                        showlegend=False,
                        paper_bgcolor='rgb(243, 243, 243)',
                        plot_bgcolor='rgb(243, 243, 243)',
                       )
    fig.write_html(path_to_save+'/box_plot.html')
    
class SA:

    """ Contains essential function for SA 
    
    Attributes:
        comm : MPI communication object
        rank (int): ID of each processor
        free_params (dict): Content of free parameteres including their tags and bounds
        free_params_bounds (narray): Bounds for each free parameter
        free_params_keys (array): Names of free parameters
        param_sets (list): The list of pararameter sets created during sampling
        settings (dict): Settings of the analysis
    """

    def __init__(self,free_params,settings):
        """Generates ABM object. Receives free paramatere lists and settings.
        
        Args:
            free_params (dict): Content of free parameteres including their tags and bounds
            settings (dict): Settings of the analysis
        """
        self.settings = settings

        if self.settings["MPI_flag"]:
            from mpi4py import MPI
            self.comm = MPI.COMM_WORLD
            self.rank = self.comm.Get_rank()
            print("Number of CPUs assigned: ",self.comm.Get_size())
        else:
            self.rank = 0

        if self.rank == 0:
            self.free_params = free_params
            self.free_params_keys = list(free_params.keys())
            self.free_params_bounds = list(free_params.values())
            self.output_dir = os.path.join(self.settings["output_path"],"SA")
            print("The list of free parameters: ",self.free_params_keys)
            try:
                os.makedirs(self.output_dir)
            except OSError:
                print("Creation of the directory %s failed" % self.output_dir)
            else:
                print("Successfully created the directory %s " % self.output_dir)

    
    def sample(self):
        """Conducts
        - Uniform sampling from n-dimensional space of parameters within the bounds given as SA.free_params.
        - Creates parameter sets and outputs them

        """
        if self.rank == 0:
            
            import numpy as np
            from doepy import build 
            import sys
            self.FFD = build.frac_fact_res(self.free_params,res = 5)
             ##### create parameter sets
            self.param_sets = self.FFD.to_dict('records')
            with open(self.output_dir+'/param_sets.json','w') as file:
                file.write(json.dumps({"param_sets":self.param_sets}))
            self.lower_bounds = {}
            for tag in self.free_params:
                lower_bound = self.free_params[tag][0]
                LB = [] # lower bound for one param
                for param_set in self.param_sets:
                    flag = False
                    #print("tag {} lower bound {} param {}".format(tag,lower_bound,param_set[tag]))
                    if (round(param_set[tag],7) == lower_bound):
                        flag = True
                    LB.append(flag)
                self.lower_bounds.update({tag:LB})
                #print(param_set)
                #print(self.lower_bounds)
                
            with open(self.output_dir+'/lower_bounds.json','w') as file:
                file.write(json.dumps(self.lower_bounds))

    def run(self):
        """Runs the user given model for the parameter sets. 
        """
        if self.rank == 0:
            import numpy as np

            # reload
            with open(self.output_dir+'/param_sets.json') as file:
                self.param_sets = json.load(file)["param_sets"]
            CPU_n = self.comm.Get_size()
            shares = np.ones(CPU_n,dtype=int)*int(len(self.param_sets)/CPU_n)
            plus = len(self.param_sets)%CPU_n
            for i in range(plus):
                shares[i]+=1

            portions = []
            for i in range(CPU_n):
                start = sum(shares[0:i])
                end = start + shares[i]
                portions.append([start,end])
            paramsets = self.param_sets

        else:
            portions = None
            paramsets = None

        portion = self.comm.scatter(portions,root = 0)    
        paramsets = self.comm.bcast(paramsets,root = 0) 

        def run_model(start,end):
            pb = ProgressBar(end-start)
            distances = []
            for i in range(start,end):
                replicas = []
                flag = True
                for j in range(self.settings["replica_n"]):
                    distance_replica = self.settings["model"](paramsets[i]).run()
                    if distance_replica is None:
                        distances.append(None)
                        flag = False
                        break
                    else:
                        replicas.append(distance_replica)
                if flag is False:
                    continue
                distance = sum(replicas)/len(replicas)
                distances.append(distance)
                pb.update()
            pb.done()
            return distances
        distances_perCore = run_model(portion[0],portion[1])
        

        distances_stacks = self.comm.gather(distances_perCore,root = 0)
        if self.rank == 0:
            import numpy as np
            distances = np.array([])
            for stack in distances_stacks:
                distances = np.concatenate([distances,stack],axis = 0)

            np.savetxt(self.output_dir+'/distances.txt',np.array(distances),fmt='%s')
    def postprocessing(self):
        """Conducts post processing tasks. Currently it extracts top fits and posteriors and also plots scaled posteriors.  
        """
        if self.rank == 0:
            # reload 
            import numpy as np

            distances = []
            with open(self.output_dir+'/distances.txt') as file:
                for line in file:
                    line.strip()
                    try:
                        value = float(line)
                    except:
                        value = None
                    distances.append(value)
            # reload
            with open(self.output_dir+'/lower_bounds.json') as file:
                self.lower_bounds = json.load(file)
            # top fitnesses
            # top_n = self.settings["top_n"]
            fitness_values = np.array([])
            for item in distances:
                if item == None:
                    fitness = 0
                else:
                    fitness = 1 - item
                fitness_values = np.append(fitness_values,fitness)
            PTTS_values = {}
            for key,value in self.lower_bounds.items():
                PTTS_value = self.PTSS(value,fitness_values)
                PTTS_values.update({key:PTTS_value})
            
            with open(self.output_dir+'/PTTS.json','w') as file:
                file.write(json.dumps(PTTS_values))
            print("SA postprocessing completed")
    def PTSS(self,lower_bound_indices,results_array):
        # Percentage total sum of squares
        # since results_array consists replicas, it needs to be averages for averaged based on #base::SA_settings.at("replica_n_SA") **/

        import numpy as np

        overall_mean = np.mean(results_array); # The mean output
        TTS = 0; #total sum of squares TSS
        for item in results_array:
            TTS+= (item-overall_mean)**2 #calculates TSS
        

        sum_lower_bound = 0  # the sum of outputs where the parameter holds its lower bound value
        sum_upper_bound = 0

        count_lower_bound = 0 # counts the occurrence of the parameter in its lower bound value
        count_upper_bound = 0
        for Iter in range(len(results_array)):
            if lower_bound_indices[Iter] == True : # The parameter holds its lower bound value
                sum_lower_bound += results_array[Iter]
                count_lower_bound+=1
                continue;
            
            if lower_bound_indices[Iter] == False: # The parameter holds it upper bound
                sum_upper_bound += results_array[Iter]
                count_upper_bound+=1;
                continue;
            
            raise ValueError("Value of lower bound indices must be either -1 or 1")
        

        mean_lower_bound = sum_lower_bound/count_lower_bound
        mean_upper_bound = sum_upper_bound/count_upper_bound

        SSF =(mean_upper_bound-overall_mean)**2+(mean_lower_bound-overall_mean)**2
        
        if TTS == 0:
            PTSS = 0;
        else :
            PTSS = (SSF/TTS * 100)

        return PTSS
    
import time
import os
# from pprogress import ProgressBar
import json
import pathlib
import sys
current_file = pathlib.Path(__file__).parent.absolute()
from defined_params import defined_params
sys.path.insert(1,os.path.join(current_file,'..'))
from env import ABM
sys.path.insert(1,os.path.join(current_file,'..','ABC'))
from barplot_stack import Plot, Settings, trainingData

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


    
class Experiment:
    def __init__(self,model,defined_params):
        from mpi4py import MPI
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()

        if self.rank == 0:
            print("Number of CPUs assigned: ",self.comm.Get_size())
            self.defined_params = defined_params
            self.defined_params_keys = list(defined_params.keys())
            self.defined_params_bounds = list(defined_params.values())
            self.model = model

    def sample(self):
        # self.sample_n = 1;
        # for key,values in self.defined_params.items(): # calculate the number of samples
        #     self.sample_n *= len(values)
        
        return[self.defined_params]
        pass
    def run(self):
        if self.rank == 0:
            import numpy as np
            paramsets = self.sample()
            print("Running tests")
            # get the CPU info and assign tasks for each
            CPU_n = self.comm.Get_size()
            shares = np.ones(CPU_n,dtype=int)*int(len(paramsets)/CPU_n)
            plus = len(paramsets)%CPU_n
            for i in range(plus):
                shares[i]+=1
            portions = []
            for i in range(CPU_n):
                start = i*shares[i-1]
                end = start + shares[i]
                portions.append([start,end])
        else:
            portions = None
            paramsets = None

        portion = self.comm.scatter(portions,root = 0)
        paramsets = self.comm.bcast(paramsets,root = 0)

        def run_model(start,end):
            # pb = ProgressBar(end-start)
            results_perCPU = []
            for i in range(start,end):
                results = self.model(paramsets[i]).test()
                results_perCPU.append(results)
                # pb.update()
            # pb.done()
            return results_perCPU
        results_perCore = run_model(portion[0],portion[1])
        # receive results of each CPU and stack them
        results_stacks = self.comm.gather(results_perCore,root = 0)
        if self.rank == 0:
            import numpy as np

            results = np.array([])
            for stack in results_stacks:
                results = np.concatenate([results,stack],axis = 0)
            # output the  results
            with open(os.path.join(output_dir,'results.json'),'w') as file:
                file.write(json.dumps({'results':list(results)},indent=4))
    def plot(self):
        with open(os.path.join(output_dir,'results.json')) as file:
            results = json.load(file)['results']
        # print(results)
        pltObj = Plot(Settings(),output_dir)
        pltObj.plot(results,trainingData)

if __name__ == '__main__':
    working_dir = os.getcwd()
    output_dir = os.path.join(working_dir,'outputs','test')
    try:
        os.makedirs(output_dir)
    except:
        pass
    sys.path.insert(1,output_dir)
    obj = Experiment(ABM,defined_params)
    obj.run()
    obj.plot()
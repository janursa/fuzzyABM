import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
from env import ABM
ABC_path = os.path.join(current_file,'..','..','..','ABayesianC')
sys.path.insert(1,ABC_path)
from ABayesianC import tools


settings = {
	"MPI_flag": True,
	"sample_n": 1000,
	"top_n": 50,
    "replica_n": 1,
	"output_path": "outputs/ABC",
	"test": True,
	"model":ABM
}

working_dir = os.getcwd()
output_dir = os.path.join(working_dir,settings["output_path"])
try:
	os.makedirs(output_dir)
except:
	pass
sys.path.insert(1,output_dir)
from free_params import free_parameters



if __name__ == "__main__":
	obj = tools.ABC(settings=settings,free_params=free_parameters)
	obj.sample()
	obj.run()
	obj.postprocessing()
	obj.run_tests()

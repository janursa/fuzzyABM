import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
from env import ABM
ABC_path = os.path.join(current_file,'..','..','..','barneySA/barneySA')

sys.path.insert(1,ABC_path)
import tools


settings = {
	"MPI_flag": True,
    "replica_n": 2,
	"output_path": "outputs/SA",
	"model":ABM
}
working_dir = os.getcwd()
output_dir = os.path.join(working_dir,settings["output_path"])
sys.path.insert(1,output_dir)
# print(output_dir)
from free_params import free_parameters

if __name__ == "__main__":
	sa_obj = tools.SA(free_parameters,settings)
	sa_obj.sample()
	sa_obj.run()
	sa_obj.postprocessing()


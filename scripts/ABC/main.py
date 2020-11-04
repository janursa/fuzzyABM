import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
from env import ABM
ABC_path = os.path.join(current_file,'..','..','..','ABC/ABC')
sys.path.insert(1,ABC_path)
import tools


settings = {
	"MPI_flag": True,
	"sample_n": 100,
	"top_n": 100,
    "replica_n": 1,
	"output_path": "outputs",
	"test": True,
	"model":ABM
}
working_dir = os.getcwd()
output_dir = os.path.join(working_dir,settings["output_path"])
sys.path.insert(1,output_dir)
# print(output_dir)
from c_params import free_params



if __name__ == "__main__":
	obj = tools.ABC(settings=settings,free_params=free_params)
	obj.sample()
	obj.run()
	obj.postprocessing()
	obj.run_tests()


import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
from env import ABM
ABC_path = os.path.join(current_file,'..','..','..','ABC/ABC')
print(ABC_path)
sys.path.insert(1,ABC_path)
import tools


settings = {
	"MPI_flag": True,
	"sample_n": 20,
	"top_n": 2,
    "replica_n": 1,
	"output_path": "outputs",
	"plot": True,
	"test": True,
	"model":ABM
}

free_params = {
	"CD_H_t": [0.67,1],
	"MG_L_t": [2,10],
	"MG_M_t": [5,15],
	"MG_H_t": [20,40],
	"maturity_t": [0,1],
	"B_MSC_Mo": [0.00017,0.00035],
	"a_Mo": [3-10],
	"a_Diff": [1-2],
	"a_Pr": [1-2],
	"a_Pass_Mo": [0-5]
}
if __name__ == "__main__":
	obj = tools.ABC(settings=settings,free_params=free_params)
	obj.sample()
	tools.clock.start()
	obj.run()
	tools.clock.end()
	obj.postprocessing()
	obj.run_tests()


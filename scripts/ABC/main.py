import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
from env import ABM
ABC_path = os.path.join(current_file,'..','..','..','ABC/ABC/ABC')
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
	"w_mg_ph": [0.02,0.1],
	"AE_H_t": [0,0.15],
    "AE_L_t": [0,0.15],
    "B_MSC_rec": [0.001,0.005],
    "B_MSC_Pr": [0.01,0.05],
    "B_MSC_Mo": [0.001,0.003],
    "CD_H_t": [0.5,1],
    "CD_M_t1":[0.1,0.5],
    "CD_M_t2":[0.3,0.8],
    "CD_L_t": [0,0.4],
    "MG_H_t": [15,40],
    "MG_L_t1": [0,10],
    "MG_L_t2": [3,15],
    "Mo_H_v": [2,4]
}
if __name__ == "__main__":
	obj = tools.ABC(settings=settings,free_params=free_params)
	obj.sample()
	tools.clock.start()
	obj.run()
	tools.clock.end()
	obj.postprocessing()
	obj.run_tests()


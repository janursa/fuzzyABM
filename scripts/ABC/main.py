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
	"sample_n": 5000,
	"top_n": 50,
    "replica_n": 1,
	"output_path": "outputs",
	"plot": True,
	"test": True,
	"model":ABM
}

free_params = {
	## the controller's params
	"MG_L_t": [2,10],
	"MG_M_t": [5,15],
	## un checked
	# "maturity_t": [0.6,1],
	# "a_Diff": [1,5],
	# "a_m_OC": [0.5,1],
	# "a_m_ALP": [0.5,1],
	# "c_weight":[0.0001,0.001],
	# "CD_H_t": [0.67,1],
	"B_Mo": [0.00005,0.00017],
	"a_Mo": [10,30],
	# "a_c_Mo": [5,20],
	"b_BMP": [0.001,0.005],
	"b_TGF": [0.01,0.05],
	"B_Pr": [0.021,0.083],
	# "MG_H_t": [20,40],
	# "pH_t": [8.5,9.5],
	"a_TGF_nTGF":[0.067,0.2],
	# "a_BMP_nBMP":[0.033,0.1]
}
if __name__ == "__main__":
	obj = tools.ABC(settings=settings,free_params=free_params)
	obj.sample()
	tools.clock.start()
	obj.run()
	tools.clock.end()
	obj.postprocessing()
	obj.run_tests()


import pathlib
current_file = pathlib.Path(__file__).parent.absolute()
import os
path_to_env = os.path.join(current_file,'..')
import sys
sys.path.insert(1,path_to_env)
from env import ABM

import SA


settings = {
	"MPI_flag": True,
    "replica_n": 2,
	"output_path": "outputs",
	"model":ABM
}
free_params = {
	"maturity_t": [0.6,1],
	"a_Diff": [1,10],
	"a_m_OC": [0.5,1],
	"a_m_ALP": [0.5,1],
	"c_weight":[0.0000006,0.000006],
	"CD_H_t": [0.67,1],
	"B_Mo": [0.00005,0.00017],
	"a_Mo": [10,30],
	"a_c_Mo": [5,20],
	"b_BMP": [0.001,0.005],
	"b_TGF": [0.01,0.05],
	"B_Pr": [0.021,0.083],
	"MG_H_t": [20,40],
	"TGF_H_t": [2.5,25]
}
# free_params = {
# 	"CD_H_t": [0.67,1],
# 	"B_Pr": [0.021,0.083],
# 	"c_weight":[0.0000006,0.000006],
# 	"b_TGF": [0.01,0.05],
# 	"a_m_OC": [0.5,1],
# 	"a_m_ALP": [0.5,1]
# }
if __name__ == "__main__":
	sa_obj = SA.SA(free_params,settings)
	sa_obj.sample()
	sa_obj.run()
	sa_obj.postprocessing()


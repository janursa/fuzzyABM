import pathlib
import sys
import os

from free_params import free_parameters
import numpy as np
fixed_parameters = {
  "BMP_max": 2000,
  "TGF_max":60,
  "K_p_g2": 25, # average of the physiological range
  "K_p_g1": 0.0008, # average of the physiological range
  "Mg_max": 60.0,
  "BMP_0": 0.008,
  "TGF_0": 14,
  "V_max_base":(1.43*10**-7)/24, # obtained from Ribeiro
  "K_b": 11.01, # obtained from Ribeiro
  "deg_rate_BMP": np.exp(-np.log(2)/10),
  "deg_rate_TGF": np.exp(-np.log(2)/0.17),
  "B_rec": 0.003,
  "w_mg_ph": 0.021,
  "AE_a_coeff": 4.42,
  "B_Diff": 0.0014,

  ## helvia
  # "b_BMP": 0.42,
  #  "a_Mo": 5.685685685686,"B_Pr": 0.029998998999, "a_P": 2.426426426426,
  #  "B_Mo": 0.0008608108110000001,
  #  "a_c_Mo": 54.6546546546545, "a_Diff": 2.3,
  #  "pH_t": 9.209709709710001, 
  
  ##  Bere
  "b_TGF":  1127,
  "b_BMP": 0.48,
  "B_Mo": 0.0002, 
   "a_Diff": 3.2, "c_weight": 0.00016954955,
  "a_TGF_nTGF": 0.0344954954955,
  "a_BMP_nBMP": 0.0350405405405,
  "a_m_OC": 0.5365365365370001,  "a_Mo": 4.249249249249,
  "maturity_t": 0.9279279279279999, "a_m_ALP": 0.6356356356355,
  "CD_H_t": 0.756711711712, "MG_L_t": 3.945945945946, "B_Pr": 0.07415615615599999, "a_P": 16.414914914915

  ## xu
  # "b_TGF": 621, 
  # "b_BMP": .45,
  # "B_Pr": 0.04, 
  # "a_P": 1.979479479479499,
  # "B_Mo": 0.0003, 
  # "a_Diff": 4.1, # real = 8.2117117117115
  # "a_c_Mo": 19.2692692692695
  
  ## all
  # "b_TGF": 1065,
  # "b_BMP": 0.41,
  # "a_P": 3.2347347347345003,"B_Pr": 0.029316316316500002,
  # "c_weight": 0.00029738738749999995,"a_Diff": 3,
  # "a_Mo": 5.2652652652650005,  
  # "B_Mo": 0.000531981, 
  # "a_c_Mo": 40,
  # "a_Pr_Mo": 7.702702702703, "a_m_OC": 0.6744244244245, "MG_L_t": 3.753753753754,
  # "a_TGF_nTGF": 0.0472297297295,
  # "a_BMP_nBMP": 0.045198198198
}
free_parameters_averaged = {}
for key,values in free_parameters.items(): # choose a middle point in the range of the values
  if key not in fixed_parameters.keys():
    free_parameters_averaged.update({key:np.mean(values)})
parameters = {**fixed_parameters,**free_parameters_averaged}

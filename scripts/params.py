import pathlib
import sys
import os
# current_file = pathlib.Path(__file__).parent.absolute()
# print(current_file)
# print(current_file)
# sys.path.insert(1,current_file)
from free_params import free_parameters
import numpy as np
fixed_parameters = {
  "BMP_max": 2000,
  "TGF_max": 60,
  "Mg_max": 60.0,
  "BMP_0": 0,
  "TGF_0": 0,
  "B_rec": 0.003,
  "w_mg_ph": 0.021,
  "AE_a_coeff": 6.19,
  "B_Diff": 0.0014,
  ## calibrated params for Bere
  # "B_Mo": 0.0003653153155, "a_Diff": 2.342342342342, "c_weight": 0.00016954955,
  # "a_TGF_nTGF": 0.0344954954955,
  # "a_BMP_nBMP": 0.0350405405405,
  # "b_TGF": 0.045346846846999994,"b_BMP": 0.0146171171175,
  # "a_m_OC": 0.5365365365370001,  "a_Mo": 4.249249249249,
  # "maturity_t": 0.9279279279279999, "a_m_ALP": 0.6356356356355,
  # "CD_H_t": 0.756711711712, "MG_L_t": 3.945945945946, "B_Pr": 0.07415615615599999, "a_P": 16.414914914915
  ## helvia
  # "B_Pr": 0.045855855855500005,"B_Mo": 0.00745,
  # "a_P": 2.4009009009,"a_Mo": 1.1561561561559999,
  # "a_Pr_Mo": 7.167167167166999, "pH_t": 9.25575575575599

  # both
  # "B_Mo": 0.0003918418415,
  # "a_BMP_nBMP": 0.18497097097100001,
  #  "B_Pr": 0.0295025025025,
  # "a_Diff": 1.8333333333335, "a_P": 2.432432432432, "b_BMP": 0.010990990991,
  #  "b_TGF": 0.039054054054000004, "a_Mo": 7.0570570570569995          ,
  # "c_weight": 0.000453153153, "a_c_Mo": 14.5145145145145,
  # "MG_L_t": 3.8618618618619998      ,
  # "MG_H_t": 29.83983983984,  "a_TGF_nTGF": 0.09682182182150001,
  #  "a_m_OC": 0.6856856856855, "a_m_ALP": 0.8566066066065
  ## all
  # "a_P": 3.2347347347345003,"B_Pr": 0.029316316316500002,
  # "c_weight": 0.00029738738749999995,"a_Diff": 2.063063063063,
  # "b_TGF": 0.038509009009, "a_Mo": 5.2652652652650005, "b_BMP": 0.0164414414415, "B_Mo": 0.000531981,
  # "a_c_Mo": 90.790790,
  # "a_Pr_Mo": 7.702702702703, "a_m_OC": 0.6744244244245, "MG_L_t": 3.753753753754,
  #  "a_TGF_nTGF": 0.0472297297295,
  #   "a_BMP_nBMP": 0.045198198198
  ## xu
  # "B_Pr": 0.028478478478499998, "a_P": 1.979479479479499,
  # "b_BMP": 0.040427927928, "B_Mo": 0.0007144144145000001, "a_Diff": 8.2117117117115,
  # "b_TGF": 0.078545045045,
  # "a_c_Mo": 19.2692692692695
  ## helvia
   # "a_Mo": 5.685685685686,"B_Pr": 0.029998998999, "a_P": 2.426426426426,
   # "B_Mo": 0.0008608108110000001,
   # "a_c_Mo": 54.6546546546545, "a_Diff": 7.3558558558555,
   # "pH_t": 9.209709709710001, "b_BMP": 0.040720720721

}
free_parameters_averaged = {}
for key,values in free_parameters.items(): # choose a middle point in the range of the values
  if key not in fixed_parameters.keys():
    free_parameters_averaged.update({key:np.mean(values)})
parameters = {**fixed_parameters,**free_parameters_averaged}

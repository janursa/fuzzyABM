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
  "a_Pr_Mo": 4.864972994599, "pH_t": 9.004800960192,  "a_BMP_nBMP": 0.156027005401, "b_BMP": 0.0024570914185, "B_Mo": 0.000841068214,
  "a_Diff": 1.742648529706, "a_m_OC": 0.623874774955, "a_TGF_nTGF": 0.1022919583915, "b_TGF": 0.0183096619325, "a_Mo": 3.5837167433485

}
free_parameters_averaged = {}
for key,values in free_parameters.items(): # choose a middle point in the range of the values
  if key not in fixed_parameters.keys():
    free_parameters_averaged.update({key:np.mean(values)})
parameters = {**fixed_parameters,**free_parameters_averaged}
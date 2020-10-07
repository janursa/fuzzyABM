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
  "a_Pr_Mo": 1,
  "B_Diff": 0.0014,
  "a_Pr_Mo": 6.660332066413, "MG_H_t": 29.259851970394, "B_Pr": 0.043876375275000004, "B_Mo": 0.0025821664335, "a_Mo": 5.888177635527001
}
free_parameters_averaged = {}
for key,values in free_parameters.items(): # choose a middle point in the range of the values
  free_parameters_averaged.update({key:np.mean(values)})
parameters = {**fixed_parameters,**free_parameters_averaged}
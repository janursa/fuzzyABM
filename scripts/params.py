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
  # "a_BMP_nBMP": 0.18158308308299997, "b_BMP": 0.017027027027, "B_Mo": 0.000362792793,
  # "a_Diff": 1.6171171171175, "b_TGF": 0.027509009009,
  # "MG_L_t": 4.5985985985990006, "a_m_ALP": 0.805055055055, "c_weight": 0.000435135135, "a_TGF_nTGF": 0.1227162162165, "a_Mo": 5.4804804804805,
  # "maturity_t": 0.700900900901,"B_Pr": 0.0514724724725

  ## helvia
  # "a_P": 3.513513513514, "B_Pr": 0.026585585585499998, "B_Mo": 0.0006635585585,
  "B_Pr": 0.045855855855500005,"B_Mo": 0.00745,
  "a_P": 2.4009009009,"a_Mo": 1.1561561561559999,
  "a_Pr_Mo": 7.167167167166999, "pH_t": 9.25575575575599
  # "a_c_Mo": 107.00700700700699, "B_Mo": 0.000601621622,
  # "pH_t": 9.261261261261499, "b_BMP": 0.036486486486500005,

}
free_parameters_averaged = {}
for key,values in free_parameters.items(): # choose a middle point in the range of the values
  if key not in fixed_parameters.keys():
    free_parameters_averaged.update({key:np.mean(values)})
parameters = {**fixed_parameters,**free_parameters_averaged}

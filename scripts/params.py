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
 # "a_Diff": 2.8211605802905,"B_Mo": 0.0003442921465, "b_BMP": 0.014072036018, "a_BMP_nBMP": 0.160224112056,"a_m_ALP": 0.750375187594 ,
 #"a_Mo": 6.246246246246,"b_TGF": 0.0179954954955, "c_weight": 0.0004085585585,
 # "MG_L_t": 3.0930930930929996, "maturity_t": 0.7533533533535,  "a_m_OC": 0.5748248248250001, "B_Pr": 0.032233233233,
 # "a_P": 1.8153153153155, "a_TGF_nTGF": 0.1225165165165
  ## helvia
  # "B_Pr": 0.045855855855500005,"B_Mo": 0.00745,
  # "a_P": 2.4009009009,"a_Mo": 1.1561561561559999,
  # "a_Pr_Mo": 7.167167167166999, "pH_t": 9.25575575575599

  # both
  "B_Mo": 0.0003918418415,
  "a_BMP_nBMP": 0.18497097097100001,
   "B_Pr": 0.0295025025025,
  "a_Diff": 1.8333333333335, "a_P": 2.432432432432, "b_BMP": 0.010990990991,
   "b_TGF": 0.039054054054000004, "a_Mo": 7.0570570570569995          ,
  "c_weight": 0.000453153153, "a_c_Mo": 14.5145145145145,
  "MG_L_t": 3.8618618618619998      ,
  "MG_H_t": 29.83983983984,  "a_TGF_nTGF": 0.09682182182150001,
   "a_m_OC": 0.6856856856855, "a_m_ALP": 0.8566066066065
}
free_parameters_averaged = {}
for key,values in free_parameters.items(): # choose a middle point in the range of the values
  if key not in fixed_parameters.keys():
    free_parameters_averaged.update({key:np.mean(values)})
parameters = {**fixed_parameters,**free_parameters_averaged}

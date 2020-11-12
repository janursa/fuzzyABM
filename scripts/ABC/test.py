from sklearn.metrics import explained_variance_score
import numpy as np
y_true =  [0.13, 1.4, 0.37]
y_pred = [0.36, 0.81, 0.77]
var = explained_variance_score(y_true, y_pred)
print(var)
def var_manual(exp,sim):
	mean_exp = np.mean(exp)
	stds_1 = []
	stds_2 = []
	for i in range(len(exp)):
		stds_1.append((sim[i]-exp[i])**2)
		stds_2.append((exp[i]-mean_exp)**2)
	return 1 - np.sum(stds_1)/np.sum(stds_2)
def fitness(exp,sim):
	diff_squares = []
	for i in range(len(exp)):
		diff_squares.append((sim[i] - exp[i])**2/exp[i])
	return 1-np.sum(diff_squares)
print(var_manual(y_true,y_pred))
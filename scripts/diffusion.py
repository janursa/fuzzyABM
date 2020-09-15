from fipy import Variable, CellVariable, PeriodicGrid2D, Viewer, TransientTerm, DiffusionTerm, ImplicitSourceTerm
from fipy.tools import numerix

import random
import decimal
import numpy as np
doPlot = True
doWait = True
doRescale = True
class Diff:
	def __init__(self,x,y,patch_l,D,timeStepDuration,steps):
		# Domain
		self.nx = (x/patch_l)
		self.ny = (y/patch_l)
		self.patch_l = patch_l
		self.D = D # mm2/hr
		self.timeStepDuration = timeStepDuration # hr
		self.steps = steps # number of steps

		self.mesh = PeriodicGrid2D(dx=self.patch_l, dy=self.patch_l, nx=self.nx, ny=self.ny)
		self.eq = TransientTerm() == DiffusionTerm(coeff=D) 
		print("dx = {}, nx = {}".format(self.patch_l, self.nx))
	def reset(self,initialConditions):
		pinit = np.zeros(nx*ny) #TODO: how to map from the ABM domain to this form
		if initialConditions == None:
			for i in range(nx*ny):
			    pinit[i] = float(decimal.Decimal(random.randrange(8, 50))) #ng/mm3
		else:
			pass
		
		print("Initial values:")
		print(pinit)
	def run(self):
		phi = CellVariable(name = "Concentration (ng/ml)", mesh = self.mesh, value = pinit)
		t = Variable(0.)
		self.eq.solve(var=phi, dt=self.timeStepDuration)
    	t.setValue(t.value + self.timeStepDuration)
    	return phi.value
		






# # Initial conditions: 0.008 ... 0.05
# # Here randomly generated but should be defined bu the user



# # Concentration


# # Time


# # Equation


# if __name__ == '__main__' and doPlot:
#     if doRescale:
#         viewer = Viewer(vars=phi, datamin=0.)
#     else:
#         viewer = Viewer(vars=phi, datamin=0., datamax=max(pinit))
#     viewer.plot()

# for step in range(steps):
    
#     print("Time = {}".format(t.value))
# if __name__ == '__main__' and doPlot:
#     viewer.plot()
#     if doWait:
#         input("Press Enter to continue...")

# print("Final values:")
# print(phi.value)

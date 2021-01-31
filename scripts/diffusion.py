from fipy import Variable, CellVariable, PeriodicGrid3D, Viewer, TransientTerm, DiffusionTerm, ImplicitSourceTerm
from fipy.tools import numerix

import random
import decimal
import numpy as np
doPlot = True
doWait = True
doRescale = True
class Diffusion:
	def __init__(self,x,y,z,patch_l,D,timeStepDuration,steps):
		# Domain
		self.nx = int(x/patch_l)
		self.ny = int(y/patch_l)
		self.nz = int(z/patch_l)

		self.patch_l = patch_l
		self.D = D # mm2/hr
		self.timeStepDuration = timeStepDuration # hr
		self.steps = steps # number of steps

		self.mesh = PeriodicGrid3D(dx=self.patch_l, dy=self.patch_l,dz=self.patch_l, nx=self.nx, ny=self.ny,nz=self.nz)
		self.eq = TransientTerm() == DiffusionTerm(coeff=D) 
		print("dx = {}, nx = {} zx {}".format(self.patch_l, self.nx, self.nz))
	
		
	def run(self,initialConditions,step_n):
		pinit = np.zeros(self.nx*self.ny*self.nz) #TODO: how to map from the ABM domain to this form
		if initialConditions == None:
			for i in range(self.nx*self.ny*self.nz):
			    pinit[i] = float(decimal.Decimal(random.randrange(8, 50))/1000000) #ng/mm3
		else:
			pass
		
		print("Initial values:")
		print(pinit)
		phi = CellVariable(name = "Concentration (ng/ml)", mesh = self.mesh, value = pinit)
		t = Variable(0.)
		for step in range(step_n):
			print("Time = {}".format(t.value))
			self.eq.solve(var=phi, dt=self.timeStepDuration)
			t.setValue(t.value + self.timeStepDuration)
		return phi.value
D1 = 0.22e-2 / 24. # mm2/hr	
diff_obj = Diff(x=0.2,y=0.2,z=4*0.008,patch_l=0.008,D=D1,timeStepDuration=0.1,steps=10)
diff_results = diff_obj.run(initialConditions=None,step_n=10)
print(diff_results)


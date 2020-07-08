import sys
import random
import pathlib
import os
import time
import platform
current_file_path = pathlib.Path(__file__).parent.absolute()
sys.path.insert(1,current_file_path)
# sys.path.insert(1,os.path.join(current_file_path,'..','..','ABM_base','build','binds'))
if platform.system() == 'Windows':
	sys.path.insert(1,os.path.join(current_file_path,'..','build','x64-Release','binds'))
else:
	sys.path.insert(1,os.path.join(current_file_path,'..','build','binds'))
from myBinds import MSC, Dead, myEnv,grid,grid3,myPatch

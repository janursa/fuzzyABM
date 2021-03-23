
"""
Plots general functions such as ph vs Mg dosages and logistics growth function for cellular internal clock
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
from matplotlib import rcParams
rcParams["mathtext.default"]='rm'
rcParams['mathtext.fontset'] = 'stixsans'
del matplotlib.font_manager.weight_dict['roman']
import pathlib as pl
import os
import math
current_dir = pl.Path(__file__).parent.absolute()
output_dir = os.path.join(current_dir,"graphs")
line_width  = 2
axis_font = {'fontname':'Times New Roman', 'size':'17'}
title_font = {'fontname':'Times New Roman', 'size':'17'}
format = ".svg"


def plot_PR_logistics():
    
plot_PR_logistics()

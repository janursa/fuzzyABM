
"""
Plots general functions such as ph vs Mg dosages and logistics growth function for cellular internal clock
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import pathlib as pl
import os
import math
current_dir = pl.Path(__file__).parent.absolute()
output_dir = os.path.join(current_dir,"outcomes")
line_width  = 2
axis_font = {'fontname':'Arial', 'size':'17'}
title_font = {'fontname':'Arial', 'size':'15'}
format = ".svg"

def plot_PR_logistics():
    x = np.linspace(0,1,100)
    pow_values = -8*(x-0.5); 
    y = []
    for item in pow_values:
        y.append( 2/(1+math.exp(item)))
    # setting the axes at the centre
    fig = plt.figure(figsize=(3, 3))
    ax = fig.add_subplot(1, 1, 1)
    #ax.set_title('BMP membership')
    ax.set_xticks([0,0.5,1])
    ax.set_yticks([0,1,2]) 
    ax.set_xlim([0,1])
    ax.set_ylim([0,2])
    #ax.set_ylabel(r'Correction coeff. ($\Omega$)',**axis_font)
    #ax.set_xlabel('Normalized internal clock ($t_{i,n}$)',**axis_font)
    ax.xaxis.grid(True, which='major')
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))
    line1, = plt.plot(x,y,color = 'indigo',linewidth=line_width, linestyle='dashed')
    line1.set_dashes([8,2,8,2])
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig( os.path.join(output_dir,"PR_logistics"+format))
plot_PR_logistics()

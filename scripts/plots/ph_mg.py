
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


def plot_pH_Mg():
    from scipy.stats import linregress
    data = {0.93:7.8,1.46:7.8,3.50:7.9,6.08:8.04,10.13:8.09,14.36:8.17,26.67:8.35}
    x = []
    y = []
    for key,value in data.items():
        x.append(key)
        y.append(value)
    
    # setting the axes at the centre
    x = np.array(x)
    y = np.array(y)
    reg_data = linregress(x,y)
    print("regression: {}".format(reg_data))
    fig = plt.figure(figsize=(4,3))
    ax = fig.add_subplot(1, 1, 1)
    
    # ax.set_xticks([0,0.5,1])
    # ax.set_yticks([0,1,2]) 

    #ax.set_ylabel(r'Correction coeff. ($\Omega$)',**axis_font)
    #ax.set_xlabel('Normalized internal clock ($t_{i,n}$)',**axis_font)
    # ax.xaxis.grid(True, which='major')

    y_pred = reg_data.slope*x + reg_data.intercept
    # plotting the regression line 
   
    ax.scatter(x, y,  
               marker = "o", linewidths=2, label='Data',color = 'olive',edgecolors='royalblue')
    ax.plot(x, y_pred,linewidth=line_width,label='Regression',color = 'darkred') 

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))
    #ax.yaxis.grid(True, which='both')

    # plt.tick_params(axis="both",labelsize=18);
    # plot the function
    plt.grid(False)
    # ax.set_xlabel('Mg',**axis_font)
    # ax.set_ylabel('pH',**axis_font)
    
    ax.set_xlim([-1,29])
    ax.set_ylim([7.62,8.65])
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 0.2))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
    # ax.legend(bbox_to_anchor=(1,1.05),fontsize=13 ,frameon=False,ncol=2)

    handles, labels = ax.get_legend_handles_labels()
    # sort both labels and handles by labels
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    ax.legend(handles, labels,bbox_to_anchor=(.6,1),fontsize=12)
    plt.savefig( os.path.join(output_dir,"ph_Mg"+format),bbox_inches = 'tight')

plot_pH_Mg()


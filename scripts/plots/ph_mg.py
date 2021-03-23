
"""
Plots general functions such as ph vs Mg dosages and logistics growth function for cellular internal clock
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
rcParams["mathtext.default"]='rm'
rcParams['mathtext.fontset'] = 'stixsans'
del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()
import pathlib as pl
import os
import math
from scipy.stats import linregress
current_dir = pl.Path(__file__).parent.absolute()
output_dir = os.path.join(current_dir,'graphs')
line_width  = 2
axis_font = {'fontname':'Times New Roman', 'size':'17'}
title_font = {'fontname':'Times New Roman', 'size':'17'}
format = ".svg"


fig = plt.figure()
f, axes = plt.subplots(1, 2,figsize=(9,3), gridspec_kw={'width_ratios': [1,1],'wspace':0.3})

data = {0.93:7.8,1.46:7.8,3.50:7.9,6.08:8.04,10.13:8.09,14.36:8.17,26.67:8.35} # ph_Mg
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
y_pred = reg_data.slope*x + reg_data.intercept 
axes[0].scatter(x, y,  
           marker = "o", linewidths=2, label='Data',color = 'blue',edgecolors='royalblue')
axes[0].plot(x, y_pred,linewidth=line_width,label='Regression',color = 'red') 
plt.grid(False)
axes[0].set_xlim([-1,29])
axes[0].set_ylim([7.62,8.65])
start, end = axes[0].get_ylim()
axes[0].yaxis.set_ticks(np.arange(start, end, 0.2))
axes[0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
# ax.legend(bbox_to_anchor=(1,1.05),fontsize=13 ,frameon=False,ncol=2)

handles, labels = axes[0].get_legend_handles_labels()
# sort both labels and handles by labels
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
axes[0].legend(handles, labels,bbox_to_anchor=(.6,1),fontsize=12)
axes[0].set_xlabel('Mg$^{2+}$ ions (mM)',**axis_font)
axes[0].set_ylabel('pH',**axis_font)
axes[0].set_title('(A): pH versus Mg$^{2+}$ ions',**title_font,fontweight ='bold',y=1.1)
## logistic growth
x = np.linspace(0,1,100)
pow_values = -8*(x-0.5); 
y = []
for item in pow_values:
    y.append( 2/(1+math.exp(item)))
axes[1].set_title('(B): Bias function',**title_font, fontweight ='bold',y=1.1)
axes[1].set_xticks([0,0.5,1])
axes[1].set_yticks([0,1,2]) 
axes[1].set_xlim([0,1])
axes[1].set_ylim([0,2])

axes[1].xaxis.grid(True, which='major')
axes[1].yaxis.grid(True, which='major')

line1, = axes[1].plot(x,y,color = 'indigo',linewidth=line_width, linestyle='dashed')
line1.set_dashes([4,1,4,1])

axes[1].set_ylabel('Bias value ($\\Omega$)',**axis_font)
axes[1].set_xlabel('Cell\'s internal clock',**axis_font)

for ax in axes:
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))
plt.savefig( os.path.join(output_dir,"ph_Mg_logistics"+format),bbox_inches = 'tight')



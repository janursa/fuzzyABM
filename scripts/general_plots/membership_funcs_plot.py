"""
Plots membership functions for fuzzification. The `post` function takes care of plot appearence and saving.
Legends are exported seperately 
"""
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import pathlib as pl
import os
import math
import copy
import pylab
import pylab

current_dir = pl.Path(__file__).parent.absolute()
output_dir = os.path.join(current_dir,"outcomes")
line_width  = 2
axis_font = {'fontname':'Arial', 'size':'13'}
title_font = {'fontname':'Arial', 'size':'13'}
legend_font = { 'family':'Arial','size':'13'}
# colors = ['indigo','darkred','teal','royalblue','seagreen','tan']
colors = {'neg':'indigo' , 'low':'darkred', 'medium':'royalblue', 'high':'olive'}
linestyles = {'neg':'solid' , 'low':'dashed', 'medium':'dashed', 'high':'dashed'}
format = ".svg"
def plot_BMP():
    fig,ax = plt.subplots(figsize=(5.5, 3))
    range = np.arange(0, 70, .5)
    # Generate fuzzy membership functions
    neg = fuzz.trapmf(range, [0,0,0.008,0.5])
    low = fuzz.trapmf(range, [0.008,0.5,10,50])
    medium = fuzz.trapmf(range, [10,50,200,500])
    high = fuzz.trapmf(range, [200,500,2000,2000])
    fakes = {"0.008":10,"0.5":20,"10":30,"50":40,"200":50,"500":60,"2000":70}
    fake_neg = fuzz.trapmf(range, [0,0,fakes["0.008"],fakes["0.5"]])
    fake_low = fuzz.trapmf(range, [fakes["0.008"],fakes["0.5"],fakes["10"],fakes["50"]])
    fake_medium = fuzz.trapmf(range, [fakes["10"],fakes["50"],fakes["200"],fakes["500"]])
    fake_high = fuzz.trapmf(range, [fakes["200"],fakes["500"],fakes["2000"],fakes["2000"]])
    # Visualize these universes and membership functions
    line1, = ax.plot(range, fake_neg, colors['neg'], linewidth=line_width, label='N',linestyle=linestyles['neg'])
    line2, = ax.plot(range, fake_low,colors['low'] , linewidth=line_width, label='L',linestyle=linestyles['low'])
    line2.set_dashes([1, 1, 1, 1])
    line3, = ax.plot(range, fake_medium, colors['medium'], linewidth=line_width, label='M',linestyle=linestyles['medium'])
    line3.set_dashes([2, 1, 2, 1])
    line4, = ax.plot(range, fake_high, colors['high'], linewidth=line_width, label='H',linestyle = linestyles['high'])
    line4.set_dashes([4, 2, 4, 2])
    #ax.set_title('BMP membership')
    ax.set_xticks([0,fakes["0.008"],fakes["0.5"],fakes["10"],fakes["50"], fakes["200"],fakes["500"],fakes["2000"]]) 
    ax.set_xticklabels([0,0.08,0.5,10,50, 200,500,2000])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Conc.($ng/ml$)',**axis_font)
    # ax.legend(loc=2, fontsize=16)
    return fig,ax,'BMP'
def plot_TGF():
    fig,ax = plt.subplots(figsize=(5, 3))
    range = np.arange(0, 60, .025)
    # Generate fuzzy membership functions
    neg_vec = [0,0,0.05,14.2]
    low_vec = [0.05,14.2,36.3,43.3]
    high_vec = [36.3,43.3,60,60]
    fakes = {0:0,0.05:8,14.2:22,36.3:36,43.3:50,60:60}
    fake_neg = fuzz.trapmf(range, [fakes[i] for i in neg_vec])
    fake_low = fuzz.trapmf(range, [fakes[i] for i in low_vec])
    fake_high = fuzz.trapmf(range, [fakes[i] for i in high_vec])
    # Visualize these universes and membership functions
    line1, = ax.plot(range, fake_neg, colors['neg'], linewidth=line_width, label='N',linestyle=linestyles['neg'])
    line2, = ax.plot(range, fake_low, colors['low'], linewidth=line_width, label='L',linestyle=linestyles['low'])
    line2.set_dashes([1, 1, 1, 1])
    line3, = ax.plot(range, fake_high, colors['high'], linewidth=line_width, label='H',linestyle = linestyles['high'])
    line3.set_dashes([2, 1, 2, 1])
    #ax.set_title('BMP membership')
    ax.set_xticks([fakes[neg_vec[1]],fakes[neg_vec[2]],fakes[neg_vec[3]],
                   fakes[low_vec[2]],fakes[low_vec[3]],
                   fakes[high_vec[2]]]) 
    ax.set_xticklabels([neg_vec[1],neg_vec[2],neg_vec[3],
                        low_vec[2],low_vec[3],
                        high_vec[2]])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Conc.($ng/ml$)',**axis_font)
    return fig,ax,r'TGF-$\beta$'
def plot_MG():
    fig = pylab.figure(figsize=(5.5, 3))
    ax = fig.add_subplot(111)
    fakes = {0.8:5,5:12,15:20,40:29,60:40} # fake positions maping
    range = np.arange(0, 40, .5)
    # Generate fuzzy membership functions
    neg = fuzz.trapmf(range, [0,0,0.8,5])
    low = fuzz.trimf(range, [0.8,5,15])
    medium = fuzz.trimf(range, [5,15,40])
    high = fuzz.trapmf(range, [15,40,60,60])
    # fake the values
    fake_neg = fuzz.trapmf(range, [0,0,fakes[0.8],fakes[5]])
    fake_low = fuzz.trimf(range, [fakes[0.8],fakes[5],fakes[15]])
    fake_medium = fuzz.trimf(range, [fakes[5],fakes[15],fakes[40]])
    fake_high = fuzz.trapmf(range, [fakes[15],fakes[40],fakes[60],fakes[60]])
    # Visualize these universes and membership functions
    line1, =ax.plot(range, fake_neg,colors['neg'], linewidth=line_width, label='N',linestyle=linestyles['neg'])
    line2, =ax.plot(range, fake_low, colors['low'], linewidth=line_width, label='L',linestyle=linestyles['low'])
    line2.set_dashes([1, 1, 1, 1])
    line3, =ax.plot(range, fake_medium, colors['medium'], linewidth=line_width, label='M',linestyle=linestyles['medium'])
    line3.set_dashes([2, 1, 2, 1])
    line4, =ax.plot(range, fake_high, colors['high'], linewidth=line_width, label='H',linestyle=linestyles['high'])
    line4.set_dashes([4, 2, 4, 2])
    #ax.set_title('BMP membership')
    ax.set_xticks([0,fakes[0.8],fakes[5],fakes[15],fakes[40],fakes[60]]) 
    ax.set_xticklabels([0,0.8,r'$c_{mlt}$',r'$c_{mmt}$',r'$c_{mht}$',60])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Conc.(mM)',**axis_font)
    return fig,ax,'Mg'
def plot_CD():
    fig,ax = plt.subplots(figsize=(5, 3))
    range = np.arange(0, 1, 0.01)
    # Generate fuzzy membership functions
    low = fuzz.trapmf(range, [0,0,0.15, 0.33])
    medium = fuzz.trapmf(range, [0.15, 0.33,0.6,0.78])
    high = fuzz.trapmf(range, [0.6,0.78,1,1])
    # Visualize these universes and membership functions
    line1, = ax.plot(range, low, colors['low'], linewidth=line_width, label='L',linestyle=linestyles['low'])
    line1.set_dashes([1,1,1,1])
    line2, = ax.plot(range, medium, colors['medium'], linewidth=line_width, label='M',linestyle = linestyles['medium'])
    line2.set_dashes([2,1,2,1])
    line3, = ax.plot(range, high, colors['high'], linewidth=line_width, label='H',linestyle=linestyles['high'])
    line3.set_dashes([4,2,4,2])
    #ax.set_title('BMP membership')
    ax.set_xticks([0, 0.15, 0.33,0.6,0.78,1]) 
    ax.set_xticklabels([0, 0.07, 0.11,r'$c_{cmt}$',r'$c_{cht}$',1])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Density',**axis_font)
    return fig,ax,'Cell density'
def plot_AE():
    fig,ax = plt.subplots(figsize=(4, 3))
    range = np.arange(0, 1, .01)
    # Generate fuzzy membership functions
    low = fuzz.trapmf(range, [0,0,0.16,1])
    high = fuzz.trapmf(range, [0,0,1,1])
    # Visualize these universes and membership functions
    line2, = ax.plot(range, low, colors['low'], linewidth=line_width, label='L', linestyle = linestyles['low'])
    line2.set_dashes([1,1,1,1])
    line4, = ax.plot([0,0.16,1], [0,0,1], colors['high'], linewidth=line_width, label='H',linestyle = linestyles['high'])
    line4.set_dashes([4,2,4,2])
    ax.set_xticks([0,0.16,1]) 
    ax.set_xticklabels([0,0.16,1])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Intensity',**axis_font)
    return fig,ax,'Alkalinization effect'
def plot_maturity():
    fig,ax = plt.subplots(figsize=(4, 3))
    range = np.arange(0, 1, .01)
    # Generate fuzzy membership functions
    low = fuzz.trimf(range, [0,0,1])
    high = fuzz.trimf(range, [0,1,1])
    # Visualize these universes and membership functions
    line2, = ax.plot(range, low, colors['low'], linewidth=line_width, label='L', linestyle = linestyles['low'])
    line2.set_dashes([1,1,1,1])
    line4, = ax.plot(range, high, colors['high'], linewidth=line_width, label='H',linestyle = linestyles['high'])
    line4.set_dashes([4,2,4,2])
    ax.set_xticks([0,1]) 
    ax.set_xticklabels([0,1])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Normalized value',**axis_font)
    return fig,ax,'Maturity'
def post(ax,name):
    """
    This function takes the fig and also the name of the plot and does post processing as well as saving the fig.
    """
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))
    ax.set_title(name,**title_font,fontweight='bold')
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    # ax.get_legend().remove()
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,prop=legend_font)
    plt.tight_layout()
    plt.savefig( os.path.join(output_dir,name+format))

## plot BMP
fig,ax,name = plot_BMP()
post( ax,name)
## plot TGF
fig,ax,name = plot_TGF()
post( ax,name)
## plot CD
fig,ax,name = plot_CD()
post( ax,name)
## plot AE
fig,ax,name = plot_AE()
post( ax,name)
## plot maturity
fig,ax,name = plot_maturity()
post( ax,name)
## plot MG
fig,ax,name = plot_MG()
post( ax,name)

def export_legend(axes):
    figLegend = pylab.figure(figsize = (1.5,1.3))
    pylab.figlegend(*axes.get_legend_handles_labels(), loc = 'upper left')
    figLegend.savefig(os.path.join(output_dir,'legend.svg'))
export_legend(ax)






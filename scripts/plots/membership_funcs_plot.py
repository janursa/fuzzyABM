"""
Plots membership functions for fuzzification. The `post` function takes care of plot appearence and saving.
Legends are exported seperately 
"""
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pathlib as pl
import os
import math
import copy
import pylab
import pylab
import matplotlib.font_manager
rcParams["mathtext.default"]='rm'
file_dir = pl.Path(__file__).parent.absolute()
output_dir = os.path.join(file_dir,"graphs")
line_width  = 2
axis_font = {'fontname':'Times New Roman', 'size':'18'}
title_font = {'fontname':'Times New Roman', 'size':'20'}
legend_font = { 'family':'Times New Roman','size':'18'}
# colors = ['indigo','darkred','teal','royalblue','seagreen','tan']
colors = {'neg':'indigo' , 'low':'darkred', 'medium':'royalblue', 'high':'olive','veryhigh':'red'}
linestyles = {'neg':'solid' , 'low':'dashed', 'medium':'dashed', 'high':'dashed','veryhigh':'dashed'}
format = ".svg"

def plot_BMP():
    fig,ax = plt.subplots(figsize=(5.5, 3))
    range = np.arange(0, 70, .5)
    # Generate fuzzy membership functions
    neg = fuzz.trapmf(range, [0,0,0.008,10])
    low = fuzz.trapmf(range, [0.008,10,20,50])
    medium = fuzz.trapmf(range, [20,50,200,500])
    high = fuzz.trapmf(range, [200,500,2000,2000])
    fakes = {"0.008":10,"10":20,"20":30,"50":40,"200":50,"500":60,"2000":70}
    fake_neg = fuzz.trapmf(range, [0,0,fakes["0.008"],fakes["10"]])
    fake_low = fuzz.trapmf(range, [fakes["0.008"],fakes["10"],fakes["20"],fakes["50"]])
    fake_medium = fuzz.trapmf(range, [fakes["20"],fakes["50"],fakes["200"],fakes["500"]])
    fake_high = fuzz.trapmf(range, [fakes["200"],fakes["500"],fakes["2000"],fakes["2000"]])
    # Visualize these universes and membership functions
    line1, = ax.plot(range, fake_neg, colors['neg'], linewidth=line_width, label='N',linestyle=linestyles['neg'])
    line2, = ax.plot(range, fake_low,colors['low'] , linewidth=line_width, label='L',linestyle=linestyles['low'])
    line2.set_dashes([1, 1, 1, 1])
    line3, = ax.plot(range, fake_medium, colors['medium'], linewidth=line_width, label='M',linestyle=linestyles['medium'])
    line3.set_dashes([2, 1, 2, 1])
    line4, = ax.plot(range, fake_high, colors['high'], linewidth=line_width, label='H',linestyle = linestyles['high'])
    line4.set_dashes([4, 2, 4, 2])
    # ax.set_title('BMP2',fontname = 'Times New Roman Bold',size = 17)
    ax.set_xticks([0,fakes["0.008"],fakes["10"],fakes["20"],fakes["50"], fakes["200"],fakes["500"],fakes["2000"]]) 
    ax.set_xticklabels([0,0.008,10,20,50, 200,500,2000])
    ax.set_yticks([0,0.5,1])
    ax.set_yticklabels([0,0.5,1])
    # ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Concentration (ng/ml)',**axis_font)
    tags_x_locs = [(0+fakes["0.008"])/2,(fakes["10"]+fakes["20"])/2,(fakes["50"]+fakes["200"])/2,(fakes["500"]+fakes["2000"])/2]
    tags = ['Negligible','Stimulatory','High','Destructive']
    # ax.legend(loc=2, fontsize=16)
    return fig,ax,'BMP2',tags_x_locs,tags
def plot_TGF():
    fig,ax = plt.subplots(figsize=(4.2, 3))
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
    # ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Concentration (ng/ml)',**axis_font)

    tags_x_locs = [6,
    (fakes[low_vec[1]]+fakes[low_vec[2]])/2,(fakes[high_vec[1]]+fakes[high_vec[2]])/2]
    tags = ['Negligible','Stimulatory','High']
    return fig,ax,r'TGF-$\beta$1',tags_x_locs,tags
def plot_MG():
    fig = pylab.figure(figsize=(6.5, 3))
    ax = fig.add_subplot(111)
    fakes = {0.8:3,1.8:6,5:12,15:23,40:32,60:40} # fake positions maping
    range = np.arange(0, 40, .5)
    # Generate fuzzy membership functions
    neg = fuzz.trapmf(range, [0,0,0.8,5])
    neg_low = fuzz.trimf(range, [0,5,10])
    low = fuzz.trimf(range, [5,10,15])
    medium = fuzz.trimf(range, [10,15,40])
    high = fuzz.trapmf(range, [15,40,60,60])
    # fake the values
    fake_neg = fuzz.trapmf(range, [0,0,fakes[0.8],fakes[1.8]])
    fake_neg_low = fuzz.trapmf(range, [fakes[1.8],fakes[40],fakes[60],fakes[60]])
    fake_low = fuzz.trimf(range, [fakes[0.8],fakes[5],fakes[15]])
    fake_medium = fuzz.trimf(range, [fakes[5],fakes[15],fakes[40]])
    fake_high = fuzz.trapmf(range, [fakes[15],fakes[40],fakes[60],fakes[60]])
    # Visualize these universes and membership functions
    line1, =ax.plot(range, fake_neg,colors['neg'], linewidth=line_width, label='N',linestyle=linestyles['neg'])
    line1_2, =ax.plot(range, fake_neg_low, colors['low'], linewidth=line_width, label='L',linestyle=linestyles['low'])
    line1_2.set_dashes([1, 1, 1, 1])
    line2, =ax.plot(range, fake_low, colors['medium'], linewidth=line_width, label='L',linestyle=linestyles['medium'])
    line2.set_dashes([2, 1, 2, 1])
    line3, =ax.plot(range, fake_medium, colors['high'], linewidth=line_width, label='M',linestyle=linestyles['high'])
    line3.set_dashes([4, 2, 4, 2])
    line4, =ax.plot(range, fake_high, colors['veryhigh'], linewidth=line_width, label='H',linestyle=linestyles['veryhigh'])
    line4.set_dashes([8, 2, 8, 2])
    #ax.set_title('BMP membership')
    ax.set_xticks([0,fakes[0.8],fakes[1.8],fakes[5],fakes[15],fakes[40],fakes[60]]) 
    ax.set_xticklabels([0,0.8,1.8,r'$c_{mlt}$',r'$c_{mmt}$',r'$c_{mht}$',60])
    # ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Concentration (mM)',**axis_font)
    tags_x_locs = [(0+fakes[0.8])/2,fakes[1.8],fakes[5],fakes[15],(fakes[40]+fakes[60])/2]
    tags = ['Negligible','Inhibitory','Stimulatory','High','Destructive']
    return fig,ax,r'Mg$^{2+}$ ions',tags_x_locs,tags
def plot_CD():
    fig,ax = plt.subplots(figsize=(4.5, 3))
    range = np.arange(0, 1, 0.01)
    # Generate fuzzy membership functions
    low = fuzz.trapmf(range, [0,0,0.15, 0.33])
    medium = fuzz.trapmf(range, [0.15, 0.33,0.6,0.78])
    high = fuzz.trapmf(range, [0.6,0.78,1,1])
    # Visualize these universes and membership functions
    line1, = ax.plot(range, low, colors['neg'], linewidth=line_width, label='L',linestyle=linestyles['neg'])
    
    line2, = ax.plot(range, medium, colors['low'], linewidth=line_width, label='M',linestyle = linestyles['low'])
    line2.set_dashes([1,1,1,1])
    line3, = ax.plot(range, high, colors['medium'], linewidth=line_width, label='H',linestyle=linestyles['medium'])
    line3.set_dashes([4,2,4,2])
    #ax.set_title('BMP membership')
    ax.set_xticks([0, 0.15, 0.33,0.6,0.78,1]) 
    ax.set_xticklabels([0, r'$c_{clt1}$', r'$c_{clt2}$',r'$c_{cht1}$',r'$c_{cht2}$',1])
    # ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Unitless quantity',**axis_font)
    tags_x_locs = [0.075,.46,0.9]
    tags = ['Isolating','Favorable','Pressing']
    return fig,ax,'Cell density',tags_x_locs,tags
def plot_AE(): 
    fig,ax = plt.subplots(figsize=(4, 3))
    range = np.arange(0, 1, .01)
    # Generate fuzzy membership functions
    low = fuzz.trimf(range, [0,0,.5])
    medium = fuzz.trimf(range, [0,.5,1])
    high = fuzz.trimf(range, [.5,1,1])
    # Visualize these universes and membership functions
    line1, = ax.plot(range, low, colors['neg'], linewidth=line_width, label='L', linestyle = linestyles['neg'])
    # line1.set_dashes([1,1,1,1])
    line2, = ax.plot(range, medium, colors['low'], linewidth=line_width, label='L', linestyle = linestyles['low'])
    line2.set_dashes([1,1,1,1])
    line4, = ax.plot(range, high, colors['medium'], linewidth=line_width, label='H',linestyle = linestyles['medium'])
    line4.set_dashes([4,2,4,2])
    ax.set_xticks([0,0.5,1]) 
    ax.set_xticklabels([0,r'$A_{t}$',1])
    # ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Intensity',**axis_font)
    tags_x_locs = [.125,.5,0.875]
    tags = ['Low','Mild','Severe']
    return fig,ax,'Alkalinity',tags_x_locs,tags
def plot_maturity():
    fig,ax = plt.subplots(figsize=(3.5, 3))
    range = np.arange(0, 1, .01)
    # Generate fuzzy membership functions
    low = fuzz.trimf(range, [0,0,1])
    high = fuzz.trimf(range, [0,1,1])
    # Visualize these universes and membership functions
    line2, = ax.plot(range, low, colors['neg'], linewidth=line_width, label='L', linestyle = linestyles['neg'])
    line4, = ax.plot(range, high, colors['low'], linewidth=line_width, label='H',linestyle = linestyles['low'])
    line4.set_dashes([1,1,1,1])
    ax.set_xticks([0,1]) 
    ax.set_xticklabels([0,1])
    # ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Unitless quantity',**axis_font)
    tags_x_locs = [.125,0.875]
    tags = ['MSC','Osteoblast']
    return fig,ax,'Maturity',tags_x_locs,tags
def post(ax,name,tags_x_locs,tags):
    """
    This function takes the fig and also the name of the plot and does post processing as well as saving the fig.
    """
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))
    ax.set_title(name,**title_font,fontweight='bold')
    ax.title.set_position([.5, 1.25])
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    # ax.get_legend().remove()
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,prop=legend_font)
    # plt.tight_layout()
    # 
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.subplots_adjust(left=0.11, right=0.95,bottom=0.25, top=0.7)
    ax.set_ylim([0,1.05])
    for i in range(len(tags)): 
        tags_x_loc = tags_x_locs[i]
        tag = tags[i]
        cs = list(colors.values())
        pos = 1.1
        if tag == 'Inhibitory':
            tags_x_loc = tags_x_loc+4
            pos = 0.1
            ax.text(tags_x_loc,pos,tag,size = 17, color = cs[i], rotation=20, fontname = 'Times New Roman',
               horizontalalignment='center',
            verticalalignment='bottom')
        else:
            ax.text(tags_x_loc,pos,tag,size = 17, color = cs[i], rotation='horizontal', fontname = 'Times New Roman',
               horizontalalignment='center',
            verticalalignment='bottom')

    plt.savefig( os.path.join(output_dir,name+format))
def plot_legends():
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
    line1, =ax.plot(range, fake_neg,colors['neg'], linewidth=line_width, label='Negligible',linestyle=linestyles['neg'])
    line2, =ax.plot(range, fake_low, colors['low'], linewidth=line_width, label='Low',linestyle=linestyles['low'])
    line2.set_dashes([1, 1, 1, 1])
    line3, =ax.plot(range, fake_medium, colors['medium'], linewidth=line_width, label='medium',linestyle=linestyles['medium'])
    line3.set_dashes([2, 1, 2, 1])
    line4, =ax.plot(range, fake_high, colors['high'], linewidth=line_width, label='High',linestyle=linestyles['high'])
    line4.set_dashes([4, 2, 4, 2])
    #ax.set_title('BMP membership')
    ax.set_xticks([0,fakes[0.8],fakes[5],fakes[15],fakes[40],fakes[60]]) 
    ax.set_xticklabels([0,0.8,r'$c_{mlt}$',r'$c_{mmt}$',r'$c_{mht}$',60])
    # ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Concentration (mM)',**axis_font)
    return fig,ax,'legends'
## plot BMP
fig,ax,name,tags_x_locs,tags = plot_BMP()
post( ax,name,tags_x_locs,tags)
## plot TGF
fig,ax,name,tags_x_locs,tags = plot_TGF()
post( ax,name,tags_x_locs,tags )
## plot CD
fig,ax,name,tags_x_locs,tags = plot_CD()
post( ax,name,tags_x_locs,tags )
# plot AE
fig,ax,name,tags_x_locs,tags = plot_AE()
post( ax,name,tags_x_locs,tags)
# plot maturity
fig,ax,name,tags_x_locs,tags = plot_maturity()
post( ax,name,tags_x_locs,tags)
## plot MG
fig,ax,name,tags_x_locs,tags= plot_MG()
post( ax,name,tags_x_locs,tags)
fig,ax,name = plot_legends()
# post( ax,name)

def export_legend(axes):
    figLegend = pylab.figure(figsize = (1.5,1.3))
    pylab.figlegend(*axes.get_legend_handles_labels(), loc = 'upper left')
    figLegend.savefig(os.path.join(output_dir,'legend.svg'))
export_legend(ax)






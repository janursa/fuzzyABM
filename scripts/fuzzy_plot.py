
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import pathlib as pl
import os
current_dir = pl.Path(__file__).parent.absolute()
line_width  = 2
axis_font = {'fontname':'Arial', 'size':'14'}
title_font = {'fontname':'Arial', 'size':'20'}
colors = {'neg':'c' , 'low':'b', 'medium':'g', 'high':'r'}
def plot_BMP():
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
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(range, fake_neg, colors['neg'], linewidth=line_width, label='Neg.')
    ax.plot(range, fake_low,colors['low'] , linewidth=line_width, label='Low')
    ax.plot(range, fake_medium, colors['medium'], linewidth=line_width, label='Medium')
    ax.plot(range, fake_high, colors['high'], linewidth=line_width, label='High')
    #ax.set_title('BMP membership')
    ax.set_xticks([0,fakes["0.008"],fakes["0.5"],fakes["10"],fakes["50"], fakes["200"],fakes["500"],fakes["2000"]]) 
    ax.set_xticklabels([0,0.008,0.5,10,50, 200,500,2000])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Conc.($ng/ml$)',**axis_font)
    ax.legend()

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))
    ax.set_title('BMP',**title_font,fontweight='bold')
    # Turn off top/right axes

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.get_legend().remove()
    plt.tight_layout()
    plt.savefig( os.path.join(current_dir,"BMP.png"))
plot_BMP()

def plot_TGF():
    range = np.arange(0, 60, .025)

    # Generate fuzzy membership functions
    neg = fuzz.trapmf(range, [0,0,0.01,0.1])
    low = fuzz.trapmf(range, [0.01,0.1,25,45])
    high = fuzz.trapmf(range, [25,45,60,60])
    fake_neg = fuzz.trapmf(range, [0,0,5,12])
    fake_low = fuzz.trapmf(range, [5,12,40,55])
    fake_high = fuzz.trapmf(range, [40,55,60,60])


    # Visualize these universes and membership functions
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(range, fake_neg, colors['neg'], linewidth=line_width, label='Neg.')
    ax.plot(range, fake_low, colors['low'], linewidth=line_width, label='Low')
    ax.plot(range, fake_high, colors['high'], linewidth=line_width, label='High')
    #ax.set_title('BMP membership')
    ax.set_xticks([0,5,12,40,55,60]) 
    ax.set_xticklabels([0,0.01,0.1,r'$c_{TGF,h}$',45,60])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Conc.($ng/ml$)',**axis_font)
    ax.set_title(r'TGF-$\beta$',**title_font,fontweight='bold')
    ax.legend()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))


    # Turn off top/right axes

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    plt.tight_layout()
    plt.savefig( os.path.join(current_dir,"TGF.png"))
plot_TGF()
def plot_MG():
    fakes = {0.8:5,5:10,15:20,40:30,60:40}
    range = np.arange(0, 40, .5)

    # Generate fuzzy membership functions
    neg = fuzz.trapmf(range, [0,0,0.8,5])
    low = fuzz.trimf(range, [0.8,5,15])
    medium = fuzz.trimf(range, [5,15,40])
    high = fuzz.trapmf(range, [15,40,60,60])

    fake_neg = fuzz.trapmf(range, [0,0,fakes[0.8],fakes[5]])
    fake_low = fuzz.trimf(range, [fakes[0.8],fakes[5],fakes[15]])
    fake_medium = fuzz.trimf(range, [fakes[5],fakes[15],fakes[40]])
    fake_high = fuzz.trapmf(range, [fakes[15],fakes[40],fakes[60],fakes[60]])


    # Visualize these universes and membership functions
    fig, ax = plt.subplots(figsize=(5, 3))

    ax.plot(range, fake_neg,colors['neg'], linewidth=line_width, label='Neg.')
    ax.plot(range, fake_low, colors['low'], linewidth=line_width, label='Low')
    ax.plot(range, fake_medium, colors['medium'], linewidth=line_width, label='Medium')
    ax.plot(range, fake_high, colors['high'], linewidth=line_width, label='High')
    #ax.set_title('BMP membership')
    ax.set_xticks([0,fakes[0.8],fakes[5],fakes[15],fakes[40],fakes[60]]) 
    ax.set_xticklabels([0,0.8,r'$c_{Mg,l}$',r'$c_{Mg,m}$',r'$c_{Mg,h}$',60])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Conc.(mM)',**axis_font)
    ax.legend()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))

    # Turn off top/right axes
    ax.get_legend().remove()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_title('Mg',**title_font,fontweight='bold')
    plt.tight_layout()
    plt.savefig( os.path.join(current_dir,"Mg.png"))
plot_MG()


def plot_CD():
    range = np.arange(0, 1, 0.01)

    # Generate fuzzy membership functions
    low = fuzz.trapmf(range, [0,0,0.15, 0.33])
    medium = fuzz.trapmf(range, [0.15, 0.33,0.6,0.78])
    high = fuzz.trapmf(range, [0.6,0.78,1,1])


    # Visualize these universes and membership functions
    fig, ax = plt.subplots(figsize=(5, 3))

    ax.plot(range, low, colors['low'], linewidth=line_width, label='Low')
    ax.plot(range, medium, colors['medium'], linewidth=line_width, label='Medium')
    ax.plot(range, high, colors['high'], linewidth=line_width, label='High')
    #ax.set_title('BMP membership')
    ax.set_xticks([0, 0.15, 0.33,0.6,0.78,1]) 
    ax.set_xticklabels([0, 0.22, 0.33,r'$CD_{m,t}$',r'$CD_{h,t}$',1])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Neighbor density',**axis_font)
    ax.legend()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))
    # Turn off top/right axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.get_legend().remove()
    ax.set_title('Cell density',**title_font,fontweight='bold')
    plt.tight_layout()
    plt.savefig( os.path.join(current_dir,"CD.png"))
plot_CD()

def plot_AE():
    range = np.arange(0, 1, .05)

    # Generate fuzzy membership functions
    low = fuzz.trimf(range, [0,0,1])
    high = fuzz.trimf(range, [0,1,1])

    # Visualize these universes and membership functions
    fig, ax = plt.subplots(figsize=(5, 3))

    ax.plot(range, low, 'b', linewidth=line_width, label='Low')
    ax.plot(range, high, 'r', linewidth=line_width, label='High')
    #ax.set_title('BMP membership')
    ax.set_xticks([0,1]) 
    ax.set_xticklabels([0,1])
    ax.set_ylabel('Membership')
    ax.set_xlabel('AE')
    ax.legend()


    # Turn off top/right axes

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    plt.tight_layout()
    plt.savefig( os.path.join(current_dir,"AE.png"))
plot_AE()

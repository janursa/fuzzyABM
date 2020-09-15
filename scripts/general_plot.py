
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import pathlib as pl
import os
import math
current_dir = pl.Path(__file__).parent.absolute()
output_dir = os.path.join(current_dir,"general_plots")
line_width  = 2
axis_font = {'fontname':'Arial', 'size':'22'}
title_font = {'fontname':'Arial', 'size':'16'}
colors = {'neg':'c' , 'low':'b', 'medium':'g', 'high':'r'}
format = ".svg"
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
    plt.savefig( os.path.join(output_dir,"BMP"+format))
plot_BMP()

def plot_TGF():
    range = np.arange(0, 60, .025)

    # Generate fuzzy membership functions
    neg_vec = [0,0,0.05,14.2]
    low_vec = [0.05,14.2,36.3,43.3]
    high_vec = [36.3,43.3,60,60]
    fakes = {0:0,0.05:10,14.2:25,36.3:40,43.3:50,60:60}
    fake_neg = fuzz.trapmf(range, [fakes[i] for i in neg_vec])
    fake_low = fuzz.trapmf(range, [fakes[i] for i in low_vec])
    fake_high = fuzz.trapmf(range, [fakes[i] for i in high_vec])


    # Visualize these universes and membership functions
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(range, fake_neg, colors['neg'], linewidth=line_width, label='Neg.')
    ax.plot(range, fake_low, colors['low'], linewidth=line_width, label='Low')
    ax.plot(range, fake_high, colors['high'], linewidth=line_width, label='High')
    #ax.set_title('BMP membership')
    ax.set_xticks([fakes[neg_vec[1]],fakes[neg_vec[2]],fakes[neg_vec[3]],
                   fakes[low_vec[2]],fakes[low_vec[3]],
                   fakes[high_vec[2]]]) 
    ax.set_xticklabels([neg_vec[1],neg_vec[2],neg_vec[3],
                        low_vec[2],low_vec[3],
                        high_vec[2]])
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
    ax.get_legend().remove()
    plt.tight_layout()
    plt.savefig( os.path.join(output_dir,"TGF"+format))
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
    fig, ax = plt.subplots(figsize=(6, 3))

    ax.plot(range, fake_neg,colors['neg'], linewidth=line_width, label='Neg.')
    ax.plot(range, fake_low, colors['low'], linewidth=line_width, label='Low')
    ax.plot(range, fake_medium, colors['medium'], linewidth=line_width, label='Medium')
    ax.plot(range, fake_high, colors['high'], linewidth=line_width, label='High')
    #ax.set_title('BMP membership')
    ax.set_xticks([0,fakes[0.8],fakes[5],fakes[15],fakes[40],fakes[60]]) 
    ax.set_xticklabels([0,0.8,r'$c_{Mg,l}$',r'$c_{Mg,m}$',r'$c_{Mg,h}$',60])
    ax.set_ylabel('Membership',**axis_font)
    #ax.set_xlabel('Conc.(mM)',**axis_font)
    ax.legend(bbox_to_anchor=(1,1))
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))

    # Turn off top/right axes
    #ax.get_legend().remove()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_title('Mg',**title_font,fontweight='bold')
    plt.tight_layout()
    plt.savefig( os.path.join(output_dir,"Mg"+format),bbox_inches = 'tight')
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
    ax.set_xlabel('Normalized value',**axis_font)
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
    title_font_CD = {'fontname':'Arial', 'size':'15'}
    ax.set_title('Cell density',**title_font_CD,fontweight='bold')
    plt.tight_layout()
    plt.savefig( os.path.join(output_dir,"CD"+format))
plot_CD()

def plot_AE():
    range = np.arange(0, 1, .01)

    # Generate fuzzy membership functions
    low = fuzz.trapmf(range, [0,0,0.16,1])
    high = fuzz.trapmf(range, [0,0,1,1])

    # Visualize these universes and membership functions
    fig, ax = plt.subplots(figsize=(5, 3))

    ax.plot(range, low, colors['low'], linewidth=line_width, label='Low')
    ax.plot([0,0.16,1], [0,0,1], colors['high'], linewidth=line_width, label='High')
    ax.set_xticks([0,0.16,1]) 
    ax.set_xticklabels([0,0.16,1])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Normalized intensity',**axis_font)

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))

    # Turn off top/right axes
    #ax.get_legend().remove()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_title('AE',**title_font,fontweight='bold')
    plt.tight_layout()
    plt.savefig( os.path.join(output_dir,"AE"+format))
plot_AE()
def plot_maturity():
    range = np.arange(0, 1, .01)

    # Generate fuzzy membership functions
    low = fuzz.trimf(range, [0,0,1])
    high = fuzz.trimf(range, [0,1,1])

    # Visualize these universes and membership functions
    fig, ax = plt.subplots(figsize=(5, 3))

    ax.plot(range, low, colors['low'], linewidth=line_width, label='Low')
    ax.plot(range, high, colors['high'], linewidth=line_width, label='High')
    ax.set_xticks([0,1]) 
    ax.set_xticklabels([0,1])
    ax.set_ylabel('Membership',**axis_font)
    ax.set_xlabel('Normalized value',**axis_font)

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))

    # Turn off top/right axes
    #ax.get_legend().remove()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_title('Maturity',**title_font,fontweight='bold')
    plt.tight_layout()
    plt.savefig( os.path.join(output_dir,"maturity"+format))
plot_maturity()



def plot_PR_logistics():
    x = np.linspace(0,1,100)

    pow_values = -8*(x-0.5); 
    y = []
    for item in pow_values:
        y.append( 2/(1+math.exp(item)))

    

    # setting the axes at the centre
    fig = plt.figure()
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
    #ax.yaxis.grid(True, which='both')

    # plt.tick_params(axis="both",labelsize=18);
    # plot the function
    plt.plot(x,y,'k')
    plt.grid(True)
    plt.savefig( os.path.join(output_dir,"PR_logistics"+format),bbox_inches = 'tight')
plot_PR_logistics()



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
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    #ax.set_title('BMP membership')
    
    # ax.set_xticks([0,0.5,1])
    # ax.set_yticks([0,1,2]) 

    #ax.set_ylabel(r'Correction coeff. ($\Omega$)',**axis_font)
    #ax.set_xlabel('Normalized internal clock ($t_{i,n}$)',**axis_font)
    # ax.xaxis.grid(True, which='major')

    y_pred = reg_data.slope*x + reg_data.intercept
    # plotting the regression line 
    ax.scatter(x, y, color = "m", 
               marker = "o", linewidth=line_width, label='Empirical data')
    plt.plot(x, y_pred,linewidth=line_width,label='Linear regression') 
    ax.legend(bbox_to_anchor=(1,.3),fontsize=18 )
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font['fontname'])
        label.set_fontsize(float(axis_font['size']))
    #ax.yaxis.grid(True, which='both')

    # plt.tick_params(axis="both",labelsize=18);
    # plot the function
    plt.grid(False)
    # ax.set_xlabel('Mg',**axis_font)
    # ax.set_ylabel('pH',**axis_font)
    
    ax.set_xlim([-2,30])
    ax.set_ylim([7.6,8.5])
    plt.savefig( os.path.join(output_dir,"ph_Mg"+format),bbox_inches = 'tight')

plot_pH_Mg()


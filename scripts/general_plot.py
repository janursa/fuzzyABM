
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import math

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
    ax.set_ylabel('Adj. coeff',fontsize = 18)
    ax.set_xlabel('Normalized internal clock',fontsize = 18)
    ax.xaxis.grid(True, which='major')
    #ax.yaxis.grid(True, which='both')

    plt.tick_params(axis="both",labelsize=18);
    # plot the function
    plt.plot(x,y,'k')
    plt.grid(True)

    plt.savefig("PR_logistics.png",bbox_inches = 'tight')
plot_PR_logistics()
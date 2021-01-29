"""
Create climate stripes version 1

Reference : https://matplotlib.org/matplotblog/posts/warming-stripes/
Author    : Zachary M. Labe
Date      : 18 January 2021
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
import cmocean
import pandas as pd
import wget

directorydata = '/Users/zlabe/Data/BEST/States/'
directoryfigure = '/Users/zlabe/Documents/Research/Visualizations/Figures/Stripes/'
states = np.array(['alabama','alaska','arizona','arkansas','california','colorado','connecticut',
'delaware','florida','georgia','hawaii','idaho','illinois','indiana','iowa','kansas','kentucky',
'louisiana','maine','maryland','massachusetts','michigan','minnesota','mississippi','missouri',
'montana','nebraska','nevada','new-hampshire','new-jersey','new-mexico','new-york','north-carolina',
'north-dakota','ohio','oklahoma','oregon','pennsylvania','rhode-island','south-carolina',
'south-dakota','tennessee','texas','utah','vermont','virginia','washington','west-virginia',
'wisconsin','wyoming'])

###########################################################################
###########################################################################
# ### Collect data from BEST
# for i in range(states.shape[0]):
#     url = 'http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/%s-TAVG-Trend.txt' % states[i]
#     filename = wget.download(url,out=directorydata)
###########################################################################
###########################################################################

### Read in data
timeq = 100 # years
year = np.empty((states.shape[0],timeq*12))
mon = np.empty((states.shape[0],timeq*12))
temp = np.empty((states.shape[0],timeq*12))
for i in range(states.shape[0]):
    filename = '%s-TAVG-Trend.txt' % states[i]
    yearq,monthq,anomq = np.genfromtxt(directorydata + filename,skip_header=70,usecols=[0,1,2],
                                    unpack=True)
    year[i,:] = yearq[-timeq*12:]
    mon[i,:] = monthq[-timeq*12:]
    temp[i,:] = anomq[-timeq*12:]
tt = np.reshape(temp,(states.shape[0],timeq,12))
mean = np.nanmean(tt,axis=2)

### Set parameters
yrmin = int(year.min())
yrmax = int(year.max())
rangemin = -2
rangemax = 2
years = np.unique(year)

###########################################################################
###########################################################################
###########################################################################
### Plot climate stripes
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

for i in range(states.shape[0]):
    fig = plt.figure(figsize=(10, 1))
    
    cmap = cmocean.cm.balance
    
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    col = PatchCollection([
        Rectangle((y, 0), 1, 1)
        for y in range(yrmin,yrmax+1)])
    
    ### Data
    col.set_array(mean[i,:])
    
    ### Range
    col.set_clim(rangemin,rangemax)
    
    col.set_cmap(cmap)
    ax.add_collection(col)
    ax.set_ylim(0, 1)
    ax.set_xlim(yrmin,yrmax+1)
    
    plt.savefig(directoryfigure + '%s_stripes.png' % states[i],dpi=300)
    
### Save data
np.savetxt(directorydata + 'States_AnnualMean_BEST_%s-%s.txt' % (yrmin,yrmax),
           mean)
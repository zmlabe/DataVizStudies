"""
Create climate stripes version 2

Reference : https://matplotlib.org/matplotblog/posts/warming-stripes/
Author    : Zachary M. Labe
Date      : 26 January 2021
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
import cmocean
import palettable.scientific.diverging as dddd
import palettable.colorbrewer.diverging as cb
import pandas as pd
import wget
from matplotlib.colors import ListedColormap
import nclcmaps as ncm

### Set parameters
typeOfStripes = 'stdev'
timeq = 100 # years
# cmap = cb.RdBu_8_r.mpl_colormap
# cmap = dddd.Vik_20.mpl_colormap
cmap = ncm.cmap('NCV_blu_red')  
directorydata = '/Users/zlabe/Data/BEST/States/'
directoryfigure = '/Users/zlabe/Documents/Research/Visualizations/Figures/Stripes/%s/' % typeOfStripes
states = np.array(['alabama','alaska','arizona','arkansas','california','colorado','connecticut',
'delaware','florida','georgia','hawaii','idaho','illinois','indiana','iowa','kansas','kentucky',
'louisiana','maine','maryland','massachusetts','michigan','minnesota','mississippi','missouri',
'montana','nebraska','nevada','new-hampshire','new-jersey','new-mexico','new-york','north-carolina',
'north-dakota','ohio','oklahoma','oregon','pennsylvania','rhode-island','south-carolina',
'south-dakota','tennessee','texas','utah','vermont','virginia','washington','west-virginia',
'wisconsin','wyoming'])

### Read in data
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

### Select month or annual average
# mean = np.nanmean(tt,axis=2)
mean = tt[:,:,-1] # December

### Set parameters
yrmin = int(year.min())
yrmax = int(year.max())
years = np.unique(year)

### Set limits
if typeOfStripes == 'absMaxMin':
    rangemax = np.tile(np.nanmax(mean),len(states))
    rangemin = np.tile(np.nanmin(mean),len(states))
elif typeOfStripes == 'localMaxMin':
    rangemax = np.nanmax(mean,axis=1)
    rangemin = np.nanmin(mean,axis=1)
elif typeOfStripes == 'stdev':
    rangemax = np.nanmean(mean,axis=1) + (np.nanstd(mean,axis=1)*2)
    rangemin = np.nanmean(mean,axis=1) - (np.nanstd(mean,axis=1)*2)

###########################################################################
###########################################################################
###########################################################################
### Plot climate stripes
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

maxlimit = np.empty((states.shape[0]))
minlimit = np.empty((states.shape[0]))
rgb = np.empty((mean.shape[0],mean.shape[1],4))
for i in range(states.shape[0]):
    fig = plt.figure(figsize=(10, 1))
    
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    col = PatchCollection([
        Rectangle((y, 0), 1, 1)
        for y in range(yrmin,yrmax+1)])
    
    ### Data
    col.set_array(mean[i,:])
    
    ### Range
    minlimit[i] = rangemin[i]
    maxlimit[i] = rangemax[i]
    col.set_clim(rangemin[i],rangemax[i])
    
    col.set_cmap(cmap)
    ax.add_collection(col)
    ax.set_ylim(0, 1)
    ax.set_xlim(yrmin,yrmax+1)
    
    rgb[i,:,:] = col.to_rgba(mean[i,:],norm=False)
    
    plt.savefig(directoryfigure + '%s_stripes.png' % states[i],dpi=300)
    
### Save data
np.savetxt(directoryfigure + 'RGBA_maxLimit_BEST_%s-%s_%s.txt' % (yrmin,yrmax,typeOfStripes),
            rgb.reshape(rgb.shape[0]*rgb.shape[1],rgb.shape[2]))
np.savetxt(directoryfigure + 'States_maxLimit_BEST_%s-%s_%s.txt' % (yrmin,yrmax,typeOfStripes),
            maxlimit)
np.savetxt(directoryfigure + 'States_minLimit_BEST_%s-%s_%s.txt' % (yrmin,yrmax,typeOfStripes),
            minlimit)
np.savetxt(directoryfigure + 'States_DecemberMean_BEST_%s-%s_%s.txt' % (yrmin,yrmax,typeOfStripes),
            mean)
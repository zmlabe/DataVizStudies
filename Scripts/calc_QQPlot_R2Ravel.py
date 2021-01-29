"""
Compute r2 between distributions of the images

Reference : Kay et al. (2015, BAMS)
Author    : Zachary M. Labe
Date      : 5 January 2021
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sts
import read_LENS as LL
import calc_Utilities as UT
import seaborn as sns
from seaborn_qqplot import pplot
import statsmodels.api as sm 
import scipy.stats as stats
import math
today = '2020-11-19'

### Directory and time
directorydata = '/Users/zlabe/Data/LENS/monthly/'
directorydata2 = '/Users/zlabe/Documents/Research/Visualizations/Data/'
directoryfigure = '/Users/zlabe/Documents/Research/Visualizations/Figures/'

### Set defaults
vari = 'T2M'
years = np.arange(1920,2100+1,1)
ensembles = np.arange(0,39+1,1)
samples = 60
sliceperiod = 'DJF'
slicebase = np.arange(1951,1980+1,1)
sliceshape = 4
slicenan = 'nan'
addclimo = True
takeEnsMean = False
read_data = True

### Read in data
if read_data == True:
    lat,lon,var,ENSmean = LL.read_LENS(directorydata,vari,sliceperiod,
                            slicebase,sliceshape,addclimo,
                            slicenan,takeEnsMean)

    ### Slice period
    yearq = np.where((years >= 1991) & (years <= 2020))[0]
    vart = var[:,yearq,:,:]

    ### Calculate trends per grid box
    trends = np.empty((vart.shape[0],lat.shape[0],lon.shape[0]))
    x = np.arange(vart.shape[1])
    for ens in range(vart.shape[0]):
        for i in range(lat.shape[0]):
            for j in range(lon.shape[0]):
                mask = np.isfinite(vart[ens,:,i,j])
                y = vart[ens,:,i,j] 
                if np.sum(mask) == y.shape[0]:
                    xx = x
                    yy = y
                else:
                    xx = x[mask]
                    yy = y[mask]      
                if np.isfinite(np.nanmean(yy)):
                    trends[ens,i,j],intercepts,r_value,p_value,std_err = sts.linregress(xx,yy)
                else:
                    trends[ens,i,j] = np.nan
        print('Completed: Calculated trends for %s ensemble!' % (ens+1))
    
    ### Calculate change in temperature
    change = trends * yearq.shape[0]

### Sort data
if read_data == True:
    ens1 = np.genfromtxt(directorydata2 + 'EnsembleSelection_DifferProj_ENS-1_%s.txt' % today)
    ens2 = np.genfromtxt(directorydata2 + 'EnsembleSelection_DifferProj_ENS-2_%s.txt' % today)
    
    newens1 = np.empty((len(ens1),lat.shape[0],lon.shape[0]))
    newens2 = np.empty((len(ens2),lat.shape[0],lon.shape[0]))
    for i in range(samples):
        newens1[i,:,:] = change[int(ens1[i]),:,:]
        newens2[i,:,:] = change[int(ens2[i]),:,:]
        
    ### Northern Hemisphere (orthographic map)
    latq = np.where((lat >= 0) & ((lat <= 90)))[0]
    map1 = newens1[:,latq,:]
    map2 = newens2[:,latq,:]
    lat1 = lat[latq]
    lon1 = lon.copy()
    lon2,lat2 = np.meshgrid(lon1,lat1)
    
    ### Vectorize
    map1v = np.reshape(map1,(map1.shape[0],map1.shape[1]*map1.shape[2]))
    map2v = np.reshape(map2,(map2.shape[0],map2.shape[1]*map2.shape[2]))
    
###########################################################################
###########################################################################
###########################################################################
### Calculate new correlation coefficients
r2_ravel = np.empty((samples))
for ii in range(samples):
    x = np.sort(map1v[ii,:])
    y = np.sort(map2v[ii,:])
    slope, intercept, r, p, se = sts.linregress(x, y)
    
    r2_ravel[ii] = r**2
    
###########################################################################
###########################################################################
###########################################################################
### Read in pattern correlations
patternr2_all = np.empty((samples))
patternr2_mid = np.empty((samples))
patternr2_pole = np.empty((samples))
for i in range(samples):
     r2values = np.genfromtxt(directorydata2 + 'MapSet_3_r2regions.txt',
                              delimiter='',unpack=True)
     patternr2_all = r2values[0,:]
     patternr2_mid = r2values[1,:]
     patternr2_pole = r2values[2,:]

###########################################################################
###########################################################################
###########################################################################
### Plot graphs of stats
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 5))
        else:
            spine.set_color('none')  
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([])

fig = plt.figure()
ax = plt.subplot(111)

adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('dimgrey')
ax.spines['bottom'].set_color('dimgrey')
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.tick_params('both',length=4,width=2,which='major',color='dimgrey')

plt.plot(patternr2_all,color='deepskyblue',linewidth=2,
         label=r'\textbf{Pattern Correlation}',linestyle='--',
         dashes=(1,0.3))
plt.plot(r2_ravel,color='navy',linewidth=2,
         label=r'\textbf{Distribution Correlation}',linestyle='--',
         dashes=(1,0.3))
plt.plot(patternr2_pole,color='dimgrey',linewidth=1,
         label=r'\textbf{Polar Correlation}',linestyle='-')
plt.plot(patternr2_mid,color='crimson',linewidth=1,
         label=r'\textbf{Midlatudes Correlation}',linestyle='-')

plt.xlabel(r'\textbf{Ensemble Comparison \#}',fontsize=10,color='k')
plt.ylabel(r'\textbf{R$^{\bf{2}}$ Between Images}',fontsize=10,color='k')
plt.yticks(np.arange(0,1.1,0.1),map(str,np.round(np.arange(0,1.1,0.1),2)),size=6)
plt.xticks(np.arange(0,61,10),map(str,np.arange(0,61,10)),size=6)
plt.xlim([0,59])   
plt.ylim([0,1])

leg = plt.legend(shadow=False,fontsize=6,loc='upper center',
              bbox_to_anchor=(0.5,1.1),fancybox=True,ncol=5,frameon=False,
              handlelength=1,handletextpad=0.5)

plt.savefig(directoryfigure + 'R2_ImagesStudy_OrthoMap.png',dpi=300)

###########################################################################

fig = plt.figure()
ax = plt.subplot(111)

patternr2_combo = (patternr2_pole + patternr2_mid)/2.

adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('dimgrey')
ax.spines['bottom'].set_color('dimgrey')
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.tick_params('both',length=4,width=2,which='major',color='dimgrey')

plt.plot(patternr2_all,color='deepskyblue',linewidth=2,
         label=r'\textbf{Pattern Correlation}',linestyle='-')
plt.plot(patternr2_combo,color='crimson',linewidth=1,
         label=r'\textbf{$\sum$ Region Correlation}',linestyle='-')

plt.xlabel(r'\textbf{Ensemble Comparison \#}',fontsize=10,color='k')
plt.ylabel(r'\textbf{R$^{\bf{2}}$ Between Images}',fontsize=10,color='k')
plt.yticks(np.arange(0,1.1,0.1),map(str,np.round(np.arange(0,1.1,0.1),2)),size=6)
plt.xticks(np.arange(0,61,10),map(str,np.arange(0,61,10)),size=6)
plt.xlim([0,59])   
plt.ylim([0,0.6])

leg = plt.legend(shadow=False,fontsize=6,loc='upper center',
              bbox_to_anchor=(0.5,1.1),fancybox=True,ncol=2,frameon=False,
              handlelength=1,handletextpad=0.5)

plt.savefig(directoryfigure + 'R2Regions2All_ImagesStudy_OrthoMap.png',dpi=300)

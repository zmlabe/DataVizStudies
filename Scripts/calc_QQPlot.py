"""
Compute pattern correlation between images

Reference : Kay et al. (2015, BAMS)
Author    : Zachary M. Labe
Date      : 24 November 2020
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
directoryfigure = '/Users/zlabe/Documents/Research/Visualizations/Figures/LoopDiffer/%s/' % today

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
read_data = False

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
### Plot graphs of stats
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

plt.figure()
sm.qqplot(map1v[1],line ='q',fit=True)
plt.figure()
sm.qqplot(map2v[5],line ='q',fit=True)

plt.figure()
ax = sns.distplot(map1v[1],fit=sts.norm, kde=False, hist=True)
plt.figure()
ax = sns.distplot(map2v[5],fit=sts.norm, kde=False, hist=True)
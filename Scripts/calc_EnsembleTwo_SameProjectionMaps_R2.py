"""
Compute pattern correlation between images

Reference : Kay et al. (2015, BAMS)
Author    : Zachary M. Labe
Date      : 24 November 2020
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import cmocean
import palettable.cubehelix as cm
import scipy.stats as sts
import read_LENS as LL
from datetime import date
import calc_Utilities as UT
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

ens1 = np.genfromtxt(directorydata2 + 'EnsembleSelection_DifferProj_ENS-1_%s.txt' % today)
ens2 = np.genfromtxt(directorydata2 + 'EnsembleSelection_DifferProj_ENS-2_%s.txt' % today)

### Northern Hemisphere maps 1
changep1 = change.copy()
latq1 = np.where((lat >= 0) & ((lat <= 90)))[0]
changenh1 = changep1[:,latq1,:]   
latp1 = lat[latq1]      

### Northern Hemisphere maps 2
changep2 = change.copy()
latq2 = np.where((lat >= 14) & ((lat <= 90)))[0]
changenh2 = changep2[:,latq2,:]  
latp2 = lat[latq2]  

### Global maps 1
changeg = change.copy()
latqg = np.where((lat >= -80) & ((lat <= 80)))[0]
changegg = changeg[:,latqg,:]  
latg = lat[latqg]  

###############################################################################
###############################################################################
###############################################################################
### Calculated weighted spatial correlation
r1 = np.empty((samples))
r2 = np.empty((samples))
r3 = np.empty((samples))
r4 = np.empty((samples))
r5 = np.empty((samples))
for i in range(samples):
    e1 = int(ens1[i])
    e2 = int(ens2[i])
    weight = 'yes'
    r1[i] = UT.calc_spatialCorr(change[e1],change[e2],lat,lon,weight)**2
    r2[i] = UT.calc_spatialCorr(change[e1],change[e2],lat,lon,weight)**2
    r3[i] = UT.calc_spatialCorr(changenh1[e1],changenh1[e2],latp1,lon,weight)**2
    r4[i] = UT.calc_spatialCorr(changenh2[e1],changenh2[e2],latp2,lon,weight)**2
    r5[i] = UT.calc_spatialCorr(changegg[e1],changegg[e2],latg,lon,weight)**2
    
### Save files
np.savetxt(directorydata2 + 'MapSet_1_r2.txt',r1)
np.savetxt(directorydata2 + 'MapSet_2_r2.txt',r2)
np.savetxt(directorydata2 + 'MapSet_3_r2.txt',r3)
np.savetxt(directorydata2 + 'MapSet_4_r2.txt',r4)
np.savetxt(directorydata2 + 'MapSet_5_r2.txt',r5)

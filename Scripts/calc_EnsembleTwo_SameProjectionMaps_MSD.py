"""
Compute mean squared differences between the two maps
Reference : Kay et al. (2015, BAMS)
Author    : Zachary M. Labe
Date      : 29 January 2021
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
msd1 = np.empty((samples))
msd2 = np.empty((samples))
msd3 = np.empty((samples))
msd4 = np.empty((samples))
msd5 = np.empty((samples))

msd1max = np.empty((samples))
msd2max = np.empty((samples))
msd3max = np.empty((samples))
msd4max = np.empty((samples))
msd5max = np.empty((samples))

msd1min = np.empty((samples))
msd2min = np.empty((samples))
msd3min = np.empty((samples))
msd4min = np.empty((samples))
msd5min = np.empty((samples))

msd1median = np.empty((samples))
msd2median = np.empty((samples))
msd3median = np.empty((samples))
msd4median = np.empty((samples))
msd5median = np.empty((samples))
for i in range(samples):
    e1 = int(ens1[i])
    e2 = int(ens2[i])
    msd1[i] = np.nanmean((change[e1] - change[e2])**2)
    msd2[i] = np.nanmean((change[e1] - change[e2])**2)
    msd3[i] = np.nanmean((changenh1[e1] - changenh1[e2])**2)
    msd4[i] = np.nanmean((changenh2[e1] - changenh2[e2])**2)
    msd5[i] = np.nanmean((changegg[e1] - changegg[e2])**2)
    
    msd1max[i] = np.nanmax((change[e1] - change[e2])**2)
    msd2max[i] = np.nanmax((change[e1] - change[e2])**2)
    msd3max[i] = np.nanmax((changenh1[e1] - changenh1[e2])**2)
    msd4max[i] = np.nanmax((changenh2[e1] - changenh2[e2])**2)
    msd5max[i] = np.nanmax((changegg[e1] - changegg[e2])**2)
    
    msd1min[i] = np.nanmin((change[e1] - change[e2])**2)
    msd2min[i] = np.nanmin((change[e1] - change[e2])**2)
    msd3min[i] = np.nanmin((changenh1[e1] - changenh1[e2])**2)
    msd4min[i] = np.nanmin((changenh2[e1] - changenh2[e2])**2)
    msd5min[i] = np.nanmin((changegg[e1] - changegg[e2])**2)
    
    msd1median[i] = np.nanmedian((change[e1] - change[e2])**2)
    msd2median[i] = np.nanmedian((change[e1] - change[e2])**2)
    msd3median[i] = np.nanmedian((changenh1[e1] - changenh1[e2])**2)
    msd4median[i] = np.nanmedian((changenh2[e1] - changenh2[e2])**2)
    msd5median[i] = np.nanmedian((changegg[e1] - changegg[e2])**2)
    
### Save files
np.savetxt(directorydata2 + 'MSD/MapSet_1_ave_MSD.txt',msd1)
np.savetxt(directorydata2 + 'MSD/MapSet_2_ave_MSD.txt',msd2)
np.savetxt(directorydata2 + 'MSD/MapSet_3_ave_MSD.txt',msd3)
np.savetxt(directorydata2 + 'MSD/MapSet_4_ave_MSD.txt',msd4)
np.savetxt(directorydata2 + 'MSD/MapSet_5_ave_MSD.txt',msd5)
    
np.savetxt(directorydata2 + 'MSD/MapSet_1_max_MSD.txt',msd1max)
np.savetxt(directorydata2 + 'MSD/MapSet_2_max_MSD.txt',msd2max)
np.savetxt(directorydata2 + 'MSD/MapSet_3_max_MSD.txt',msd3max)
np.savetxt(directorydata2 + 'MSD/MapSet_4_max_MSD.txt',msd4max)
np.savetxt(directorydata2 + 'MSD/MapSet_5_max_MSD.txt',msd5max)
    
np.savetxt(directorydata2 + 'MSD/MapSet_1_min_MSD.txt',msd1min)
np.savetxt(directorydata2 + 'MSD/MapSet_2_min_MSD.txt',msd2min)
np.savetxt(directorydata2 + 'MSD/MapSet_3_min_MSD.txt',msd3min)
np.savetxt(directorydata2 + 'MSD/MapSet_4_min_MSD.txt',msd4min)
np.savetxt(directorydata2 + 'MSD/MapSet_5_min_MSD.txt',msd5min)
    
np.savetxt(directorydata2 + 'MSD/MapSet_1_median_MSD.txt',msd1median)
np.savetxt(directorydata2 + 'MSD/MapSet_2_median_MSD.txt',msd2median)
np.savetxt(directorydata2 + 'MSD/MapSet_3_median_MSD.txt',msd3median)
np.savetxt(directorydata2 + 'MSD/MapSet_4_median_MSD.txt',msd4median)
np.savetxt(directorydata2 + 'MSD/MapSet_5_median_MSD.txt',msd5median)

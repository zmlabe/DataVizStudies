"""
Compute weighted average between the two images for each ensemble pair and
every map projection

Reference : Kay et al. (2015, BAMS)
Author    : Zachary M. Labe
Date      : 12 March 2021
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

### Meshgrid of points
lon2,lat2 = np.meshgrid(lon,lat)

### Northern Hemisphere maps 1
changep1 = change.copy()
latq1 = np.where((lat >= 0) & ((lat <= 90)))[0]
changenh1 = changep1[:,latq1,:]   
latp1 = lat[latq1]    
lonp12,latp12 = np.meshgrid(lon,latp1)  

### Northern Hemisphere maps 2
changep2 = change.copy()
latq2 = np.where((lat >= 14) & ((lat <= 90)))[0]
changenh2 = changep2[:,latq2,:]  
latp2 = lat[latq2]  
lonp22,latp22 = np.meshgrid(lon,latp2)  

### Global maps 1
changeg = change.copy()
latqg = np.where((lat >= -80) & ((lat <= 80)))[0]
changegg = changeg[:,latqg,:]  
latg = lat[latqg]  
long2,latg2 = np.meshgrid(lon,latg)  

###############################################################################
###############################################################################
###############################################################################
### Calculated weighted spatial correlation
ave1 = np.empty((samples))
ave2 = np.empty((samples))
ave3 = np.empty((samples))
ave4 = np.empty((samples))
ave5 = np.empty((samples))
for i in range(samples):
    e1 = int(ens1[i])
    e2 = int(ens2[i])
    ave1[i] = UT.calc_weightedAve((change[e1]+change[e2]/2),lat2)
    ave2[i] = UT.calc_weightedAve((change[e1]+change[e2]/2),lat2)
    ave3[i] = UT.calc_weightedAve((changenh1[e1]+changenh1[e2]/2),latp12)
    ave4[i] = UT.calc_weightedAve((changenh2[e1]+changenh2[e2]/2),latp22)
    ave5[i] = UT.calc_weightedAve((changegg[e1]+changegg[e2]/2),latg2)
    
### Save files
np.savetxt(directorydata2 + 'MapSet_1_meanTemperature.txt',ave1)
np.savetxt(directorydata2 + 'MapSet_2_meanTemperature.txt',ave2)
np.savetxt(directorydata2 + 'MapSet_3_meanTemperature.txt',ave3)
np.savetxt(directorydata2 + 'MapSet_4_meanTemperature.txt',ave4)
np.savetxt(directorydata2 + 'MapSet_5_meanTemperature.txt',ave5)

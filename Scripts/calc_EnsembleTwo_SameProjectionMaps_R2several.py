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

ens1 = np.genfromtxt(directorydata2 + 'EnsembleSelection_DifferProj_ENS-1_%s.txt' % today)
ens2 = np.genfromtxt(directorydata2 + 'EnsembleSelection_DifferProj_ENS-2_%s.txt' % today)

### Northern Hemisphere maps 1
changenh1 = change.copy()
latq1 = np.where((lat >= 0) & ((lat <= 90)))[0]
changenh1 = changenh1[:,latq1,:]   
changenh1b = changenh1.copy()
changenh1c = changenh1.copy()
latp1 = lat[latq1]      

latq1b = np.where((latp1 >= 65))[0]
changenh1b[:,latq1b,:] = np.nan   

latq1c = np.where((latp1 < 65))[0]
changenh1c[:,latq1c,:] = np.nan     

### Northern Hemisphere maps 2
changenh2 = change.copy()
latq2 = np.where((lat >= 14) & ((lat <= 90)))[0]
changenh2 = changenh2[:,latq2,:]  
changenh2b = changenh2.copy()
changenh2c = changenh2.copy()
latp2 = lat[latq2]  

latq2b = np.where((latp2 >= 65))[0]
changenh2b[:,latq2b,:] = np.nan   

latq2c = np.where((latp2 < 65))[0]
changenh2c[:,latq2c,:] = np.nan   

### Global maps 1
changeg = change.copy()
latqg = np.where((lat >= -80) & ((lat <= 80)))[0]
changegg = changeg[:,latqg,:]  
changeggb = changegg.copy()
changeggc = changegg.copy()
latg = lat[latqg]  

latqgb = np.where((latg >= 65))[0]
changeggb[:,latqgb,:] = np.nan   

latqgc = np.where((latg < 65))[0]
changeggc[:,latqgc,:] = np.nan  

### Global maps all
changeb = change.copy() 
changec = change.copy() 

latqb = np.where((lat >= 65))[0]
changeb[:,latqb,:] = np.nan   

latqc = np.where((lat < 65))[0]
changec[:,latqc,:] = np.nan  

###############################################################################
###############################################################################
###############################################################################
### Calculated weighted spatial correlation
r1 = np.empty((samples))
r2 = np.empty((samples))
r3 = np.empty((samples))
r4 = np.empty((samples))
r5 = np.empty((samples))
r1b = np.empty((samples))
r2b = np.empty((samples))
r3b = np.empty((samples))
r4b = np.empty((samples))
r5b = np.empty((samples))
r1c = np.empty((samples))
r2c = np.empty((samples))
r3c = np.empty((samples))
r4c = np.empty((samples))
r5c = np.empty((samples))
for i in range(samples):
    e1 = int(ens1[i])
    e2 = int(ens2[i])
    weight = 'yes'
    r1[i] = UT.calc_spatialCorr(change[e1],change[e2],lat,lon,weight)**2
    r2[i] = UT.calc_spatialCorr(change[e1],change[e2],lat,lon,weight)**2
    r3[i] = UT.calc_spatialCorr(changenh1[e1],changenh1[e2],latp1,lon,weight)**2
    r4[i] = UT.calc_spatialCorr(changenh2[e1],changenh2[e2],latp2,lon,weight)**2
    r5[i] = UT.calc_spatialCorr(changegg[e1],changegg[e2],latg,lon,weight)**2
    
    r1b[i] = UT.calc_spatialCorr(changeb[e1],changeb[e2],lat,lon,weight)**2
    r2b[i] = UT.calc_spatialCorr(changeb[e1],changeb[e2],lat,lon,weight)**2
    r3b[i] = UT.calc_spatialCorr(changenh1b[e1],changenh1b[e2],latp1,lon,weight)**2
    r4b[i] = UT.calc_spatialCorr(changenh2b[e1],changenh2b[e2],latp2,lon,weight)**2
    r5b[i] = UT.calc_spatialCorr(changeggb[e1],changeggb[e2],latg,lon,weight)**2
    
    r1c[i] = UT.calc_spatialCorr(changec[e1],changec[e2],lat,lon,weight)**2
    r2c[i] = UT.calc_spatialCorr(changec[e1],changec[e2],lat,lon,weight)**2
    r3c[i] = UT.calc_spatialCorr(changenh1c[e1],changenh1c[e2],latp1,lon,weight)**2
    r4c[i] = UT.calc_spatialCorr(changenh2c[e1],changenh2c[e2],latp2,lon,weight)**2
    r5c[i] = UT.calc_spatialCorr(changeggc[e1],changeggc[e2],latg,lon,weight)**2
    
### Save files
np.savetxt(directorydata2 + 'MapSet_1_r2regions.txt',np.c_[r1,r1b,r1c])
np.savetxt(directorydata2 + 'MapSet_2_r2regions.txt',np.c_[r2,r2b,r2c])
np.savetxt(directorydata2 + 'MapSet_3_r2regions.txt',np.c_[r3,r3b,r3c])
np.savetxt(directorydata2 + 'MapSet_4_r2regions.txt',np.c_[r4,r4b,r4c])
np.savetxt(directorydata2 + 'MapSet_5_r2regions.txt',np.c_[r5,r5b,r5c])

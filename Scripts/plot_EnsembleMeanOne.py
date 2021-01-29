"""
Exploratory data analysis of visualization study on CESM-LENS

Reference : Kay et al. (2015, BAMS)
Author    : Zachary M. Labe
Date      : 16 November 2020
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import cmocean
import palettable.cubehelix as cm
import scipy.stats as sts
import read_LENS as LL
import read_ERA5_monthly as ER

### Directory and time
directorydata = '/Users/zlabe/Data/LENS/monthly/'
directorydata2 = '/Users/zlabe/Data/ERA5/'
directoryfigure = '/Users/zlabe/Documents/Research/Visualizations/Figures/'

### Set defaults
vari = 'T2M'
years = np.arange(1920,2100+1,1)
yearobs = np.arange(1980,2019+1,1)
sliceperiod = 'DJF'
slicebase = np.arange(1951,1980+1,1)
sliceyear = np.arange(1979,2019+1,1)
sliceshape = 4
slicenan = 'nan'
addclimo = True
takeEnsMean = False

### Turn on read data
read_data = False
read_obs = False

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
    
    ### Calculate ensemble mean
    ensmean = np.nanmean(change,axis=0)

###########################################################################
###########################################################################
###########################################################################    
### Read in data
if read_obs == True:    
    lat,lon,varo = ER.read_ERA5_monthly(vari,directorydata2,sliceperiod,sliceyear,sliceshape,addclimo,slicenan)
    
    ### Slice period
    yearq = np.where((yearobs >= 1991) & (yearobs <= 2020))[0]
    varto = varo[yearq,:,:]
    
    ### Calculate trends per grid box
    trendso = np.empty((lat.shape[0],lon.shape[0]))
    x = np.arange(varto.shape[0])
    for i in range(lat.shape[0]):
        for j in range(lon.shape[0]):
            mask = np.isfinite(varto[:,i,j])
            y = varto[:,i,j] 
            if np.sum(mask) == y.shape[0]:
                xx = x
                yy = y
            else:
                xx = x[mask]
                yy = y[mask]      
            if np.isfinite(np.nanmean(yy)):
                trendso[i,j],intercepts,r_value,p_value,std_err = sts.linregress(xx,yy)
            else:
                trendso[i,j] = np.nan
                
    ### Calculate change in temperature for observations
    changeo = trendso * varto.shape[0]
        
###########################################################################
###########################################################################
###########################################################################
### Plot variable data for trends
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

### Set limits for contours and colorbars
limit = np.arange(-6,6.1,0.1)
barlim = np.arange(-6,7,2)
cmap = cmocean.cm.balance
label = r'\textbf{Temperature [$^{\circ}$C] Change [1991-2020]}'
    
fig = plt.figure()
###########################################################################
###########################################################################
###########################################################################
var = ensmean
ax1 = plt.subplot(111)
m = Basemap(projection='ortho',lon_0=0,lat_0=90,resolution='l',
                        area_thresh=10000.)
circle = m.drawmapboundary(fill_color='k')
circle.set_clip_on(False) 
m.drawcoastlines(color='dimgrey',linewidth=0.35)

var, lons_cyclic = addcyclic(var, lon)
var, lons_cyclic = shiftgrid(180., var, lons_cyclic, start=False)
lon2d, lat2d = np.meshgrid(lons_cyclic, lat)
x, y = m(lon2d, lat2d)
   
circle = m.drawmapboundary(fill_color='white',color='dimgrey',
                  linewidth=0.7)
circle.set_clip_on(False)

cs = m.contourf(x,y,var,limit,extend='both')
        
cs.set_cmap(cmap) 


###########################################################################
cbar_ax = fig.add_axes([0.32,0.08,0.4,0.03])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=False)

cbar.set_label(label,fontsize=7,color='k',labelpad=1.4)  

cbar.set_ticks(barlim)
cbar.set_ticklabels(list(map(str,barlim)))
cbar.ax.tick_params(axis='x', size=.01,labelsize=5)
cbar.outline.set_edgecolor('dimgrey')

plt.tight_layout()
plt.subplots_adjust(wspace=0.01,hspace=0,bottom=0.14)

plt.savefig(directoryfigure + 'TrendsMean_1991-2020_Ortho.png',dpi=300)

###########################################################################
###########################################################################
###########################################################################
fig = plt.figure(figsize=(9,4))
var = ensmean
var2 = changeo
ax1 = plt.subplot(121)
m = Basemap(projection='ortho',lon_0=0,lat_0=90,resolution='l',
                        area_thresh=10000.)
circle = m.drawmapboundary(fill_color='k')
circle.set_clip_on(False) 
m.drawcoastlines(color='dimgrey',linewidth=0.35)

var, lons_cyclic = addcyclic(var, lon)
var, lons_cyclic = shiftgrid(180., var, lons_cyclic, start=False)
lon2d, lat2d = np.meshgrid(lons_cyclic, lat)
x, y = m(lon2d, lat2d)
   
circle = m.drawmapboundary(fill_color='white',color='dimgrey',
                  linewidth=0.7)
circle.set_clip_on(False)

cs = m.contourf(x,y,var,limit,extend='both')
        
cs.set_cmap(cmap) 

###########################################################################
ax1 = plt.subplot(122)
m = Basemap(projection='ortho',lon_0=0,lat_0=90,resolution='l',
                        area_thresh=10000.)
circle = m.drawmapboundary(fill_color='k')
circle.set_clip_on(False) 
m.drawcoastlines(color='dimgrey',linewidth=0.35)

var2, lons_cyclic = addcyclic(var2, lon)
var2, lons_cyclic = shiftgrid(180., var2, lons_cyclic, start=False)
lon2d, lat2d = np.meshgrid(lons_cyclic, lat)
x, y = m(lon2d, lat2d)
   
circle = m.drawmapboundary(fill_color='white',color='dimgrey',
                  linewidth=0.7)
circle.set_clip_on(False)

cs = m.contourf(x,y,var2,limit,extend='both')
        
cs.set_cmap(cmap) 


###########################################################################
cbar_ax = fig.add_axes([0.30,0.08,0.4,0.03])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=False)

cbar.set_label(label,fontsize=7,color='k',labelpad=1.4)  

cbar.set_ticks(barlim)
cbar.set_ticklabels(list(map(str,barlim)))
cbar.ax.tick_params(axis='x', size=.01,labelsize=5)
cbar.outline.set_edgecolor('dimgrey')

plt.tight_layout()
plt.subplots_adjust(wspace=0.01,hspace=0,bottom=0.14)

plt.savefig(directoryfigure + 'TrendsMean_1991-2020_EnsMean-Obs.png',dpi=300)

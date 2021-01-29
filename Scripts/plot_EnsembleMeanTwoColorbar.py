"""
Exploratory data analysis of visualization study on CESM-LENS

Reference : Kay et al. (2015, BAMS)
Author    : Zachary M. Labe
Date      : 15 November 2020
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import cmocean
import palettable.cubehelix as cm
import scipy.stats as sts
import read_LENS as LL

### Directory and time
directorydata = '/Users/zlabe/Data/LENS/monthly/'
directoryfigure = '/Users/zlabe/Documents/Research/Visualizations/Figures/'

### Set defaults
vari = 'T2M'
years = np.arange(1920,2100+1,1)
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
    
    ### Calculate ensemble mean
    ensmean = np.nanmean(change,axis=0)
        
###########################################################################
###########################################################################
###########################################################################
### Plot variable data for trends
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

### Set limits for contours and colorbars
limit1 = np.arange(-3,3.1,0.25)
barlim1 = np.arange(-3,4,1)
limit2 = np.arange(-9,9.1,0.75)
barlim2 = np.arange(-9,10,2)
cmap = cmocean.cm.balance
label = r'\textbf{Temperature [$^{\circ}$C] Change [1991-2020]}'
runs = [ensmean,ensmean]
    
fig = plt.figure(figsize=(9,4))
###########################################################################
###########################################################################
###########################################################################
var = runs[0]
ax1 = plt.subplot(1,2,1)
m = Basemap(projection='moll',lon_0=0,resolution='l',area_thresh=10000)
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

cs1 = m.contourf(x,y,var,limit1,extend='both')
        
cs1.set_cmap(cmap) 
cbar = plt.colorbar(cs1,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=False)
cbar.set_label(label,fontsize=7,color='k',labelpad=1.4)  
cbar.set_ticks(barlim1)
cbar.set_ticklabels(list(map(str,barlim1)))
cbar.ax.tick_params(axis='x', size=.01,labelsize=5)
cbar.outline.set_edgecolor('dimgrey')

###########################################################################
###########################################################################
###########################################################################
var = runs[1]
ax1 = plt.subplot(1,2,2)
m = Basemap(projection='moll',lon_0=0,resolution='l',area_thresh=10000)
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

cs2 = m.contourf(x,y,var,limit2,extend='both')
        
cs2.set_cmap(cmap)            
cbar = plt.colorbar(cs2,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=False)
cbar.set_label(label,fontsize=7,color='k',labelpad=1.4)  
cbar.set_ticks(barlim2)
cbar.set_ticklabels(list(map(str,barlim2)))
cbar.ax.tick_params(axis='x', size=.01,labelsize=5)
cbar.outline.set_edgecolor('dimgrey')

plt.tight_layout()
plt.subplots_adjust(wspace=0.01,hspace=0,bottom=0.14)

plt.savefig(directoryfigure + 'TrendsMean_1991-2020_Colorbar_a.png',dpi=300)
        

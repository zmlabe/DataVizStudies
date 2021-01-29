"""
Exploratory data analysis of visualization study on CESM-LENS

Reference : Kay et al. (2015, BAMS)
Author    : Zachary M. Labe
Date      : 5 October 2020
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
limit = np.arange(-6,6.1,0.5)
barlim = np.arange(-6,7,2)
cmap = cmocean.cm.balance
label = r'\textbf{Temperature [$^{\circ}$C] Change [1991-2020]}'
    
fig = plt.figure()
for r in range(change.shape[0]):
    var = change[r]
    
    ax1 = plt.subplot(5,8,r+1)
    m = Basemap(projection='ortho',lon_0=0,lat_0=89,resolution='l',
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
    # if any([r==0,r==4,r==8]):
    #     ax1.annotate(r'\textbf{%s}' % datasetsingleq[r],xy=(0,0),xytext=(-0.1,0.5),
    #                   textcoords='axes fraction',color='k',fontsize=9,
    #                   rotation=90,ha='center',va='center')
    # if any([r==0,r==1,r==2,r==3]):
    #     ax1.annotate(r'\textbf{%s}' % timeq[r],xy=(0,0),xytext=(0.5,1.22),
    #                   textcoords='axes fraction',color='dimgrey',fontsize=9,
    #                   rotation=0,ha='center',va='center')
    ax1.annotate(r'\textbf{[%s]}' % (r+1),xy=(0,0),xytext=(0.87,0.95),
                  textcoords='axes fraction',color='dimgrey',fontsize=4,
                  rotation=320,ha='center',va='center')

###########################################################################
cbar_ax = fig.add_axes([0.32,0.095,0.4,0.03])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=False)

cbar.set_label(label,fontsize=7,color='k',labelpad=1.4)  

cbar.set_ticks(barlim)
cbar.set_ticklabels(list(map(str,barlim)))
cbar.ax.tick_params(axis='x', size=.01,labelsize=5)
cbar.outline.set_edgecolor('dimgrey')

plt.tight_layout()
plt.subplots_adjust(wspace=0.01,hspace=0,bottom=0.14)

plt.savefig(directoryfigure + 'TrendsAllEns_1991-2020.png',dpi=300)
        

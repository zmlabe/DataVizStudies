"""
Function reads in monthly data from ERA5
 
Notes
-----
    Author : Zachary Labe
    Date   : 15 July 2020
    
Usage
-----
    [1] read_ERA5_monthly(variq,directory,sliceperiod,sliceyear,
                  sliceshape,addclimo,slicenan)
"""

def read_ERA5_monthly(variq,directory,sliceperiod,sliceyear,sliceshape,addclimo,slicenan):
    """
    Function reads monthly data from ERA5
    
    Parameters
    ----------
    variq : string
        variable to retrieve
    directory : string
        path for data
    sliceperiod : string
        how to average time component of data
    sliceyear : string
        how to slice number of years for data
    sliceshape : string
        shape of output array
    addclimo : binary
        True or false to add climatology
    slicenan : string or float
        Set missing values
        
    Returns
    -------
    lat : 1d numpy array
        latitudes
    lon : 1d numpy array
        longitudes
    var : 3d numpy array or 4d numpy array 
        [time,lat,lon] or [year,month,lat,lon]
        
    Usage
    -----
    lat,lon,var = read_ERA5_monthly(variq,directory,sliceperiod,sliceyear,
                            sliceshape,addclimo,slicenan)
    """
    print('\n>>>>>>>>>> STARTING read_ERA5_monthly function!')
    
    ### Import modules
    import numpy as np
    from netCDF4 import Dataset
    import warnings
    import calc_Utilities as UT
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=RuntimeWarning)
    
    ###########################################################################
    ### Parameters
    time = np.arange(1979,2019+1,1)
    monthslice = sliceyear.shape[0]*12
    mon = 12
    
    ###########################################################################
    ### Read in data
    filename = 'monthly/%s_1979-2019.nc' % variq
    data = Dataset(directory + filename,'r')
    lat1 = data.variables['latitude'][:]
    lon1 = data.variables['longitude'][:]
    var = data.variables['%s' % variq][-monthslice:,:,:]
    data.close()
    
    print('Years of output =',sliceyear.min(),'to',sliceyear.max())
    ###########################################################################
    ### Reshape data into [year,month,lat,lon]
    datamon = np.reshape(var,(var.shape[0]//mon,mon,
                               lat1.shape[0],lon1.shape[0]))
    
    ###########################################################################
    ### Return absolute temperature (1951-1980 baseline)
    if addclimo == True:
        varmon = datamon
        print('Completed: calculated absolute variable!')
    else:
        yearbasemin = 1981
        yearbasemax = 2010
        yearq = np.where((time >= yearbasemin) & (time<=yearbasemax))[0]
        varmon = datamon - np.nanmean(datamon[yearq,:,:,:],axis=0)
        print('Completed: calculated anomalies!')
    
    ###########################################################################
    ### Slice over months (currently = [yr,mn,lat,lon])
    ### Shape of output array
    if sliceperiod == 'annual':
        vartime = np.nanmean(varmon,axis=1)
        if sliceshape == 1:
            varshape = vartime.ravel()
        elif sliceshape == 3:
            varshape = vartime
        print('Shape of output = ', varshape.shape,[[varshape.ndim]])
        print('Completed: ANNUAL MEAN!')
    elif sliceperiod == 'DJF':
        varshape = UT.calcDecJanFeb(varmon,lat1,lon1,'surface',1)
        print('Shape of output = ', varshape.shape,[[varshape.ndim]])
        print('Completed: DJF MEAN!')
    elif sliceperiod == 'JJA':
        vartime = np.nanmean(varmon[:,5:8,:,:],axis=1)
        if sliceshape == 1:
            varshape = vartime.ravel()
        elif sliceshape == 3:
            varshape = vartime
        print('Shape of output = ', varshape.shape,[[varshape.ndim]])
        print('Completed: JJA MEAN!')
    elif sliceperiod == 'JFM':
        vartime = np.nanmean(varmon[:,0:3,:,:],axis=1)
        if sliceshape == 1:
            varshape = vartime.ravel()
        elif sliceshape == 3:
            varshape = vartime
        print('Shape of output = ', varshape.shape,[[varshape.ndim]])
        print('Completed: JFM MEAN!')
    elif sliceperiod == 'AMJ':
        vartime = np.nanmean(varmon[:,3:6,:,:],axis=1)
        if sliceshape == 1:
            varshape = vartime.ravel()
        elif sliceshape == 3:
            varshape = vartime
        print('Shape of output = ', varshape.shape,[[varshape.ndim]])
        print('Completed: AMJ MEAN!')
    elif sliceperiod == 'JAS':
        vartime = np.nanmean(varmon[:,6:9,:,:],axis=1)
        if sliceshape == 1:
            varshape = vartime.ravel()
        elif sliceshape == 3:
            varshape = vartime
        print('Shape of output = ', varshape.shape,[[varshape.ndim]])
        print('Completed: JAS MEAN!')
    elif sliceperiod == 'OND':
        vartime = np.nanmean(varmon[:,9:,:,:],axis=1)
        if sliceshape == 1:
            varshape = vartime.ravel()
        elif sliceshape == 3:
            varshape = vartime
        print('Shape of output = ', varshape.shape,[[varshape.ndim]])
        print('Completed: OND MEAN!')
    elif sliceperiod == 'none':
        vartime = varmon
        if sliceshape == 1:
            varshape = varshape.ravel()
        elif sliceshape == 3:
            varshape = np.reshape(vartime,(vartime.shape[0]*vartime.shape[1],
                                             vartime.shape[2],vartime.shape[3]))
        elif sliceshape == 4:
            varshape = varmon
        print('Shape of output =', varshape.shape, [[varshape.ndim]])
        print('Completed: ALL MONTHS!')
        
    ###########################################################################
    ### Change missing values
    if slicenan == 'nan':
        varshape[np.where(np.isnan(varshape))] = np.nan
        print('Completed: missing values are =',slicenan)
    else:
        varshape[np.where(np.isnan(varshape))] = slicenan
        
    ###########################################################################
    ### Change units
    if variq == 'SLP':
        varshape = varshape/100 # Pa to hPa
        print('Completed: Changed units (Pa to hPa)!')
    elif variq == 'T2M':
        varshape = varshape - 273.15 # K to C
        print('Completed: Changed units (K to C)!')
        
    print('>>>>>>>>>> ENDING read_ERA5_monthly function!')
    return lat1,lon1,varshape

# ### Test functions - do not use!
# import numpy as np
# import matplotlib.pyplot as plt
# variq = 'T2M'
# directory = '/Users/zlabe/Data/ERA5/'
# sliceperiod = 'OND'
# sliceyear = np.arange(1979,2019+1,1)
# sliceshape = 3
# slicenan = 'nan'
# addclimo = True
# lat,lon,var = read_ERA5_monthly(variq,directory,sliceperiod,
#                                 sliceyear,sliceshape,addclimo,
#                                 slicenan)
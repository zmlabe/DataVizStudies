"""
Exploratory data analysis of visualization study on CESM-LENS

Reference : Kay et al. (2015, BAMS)
Author    : Zachary M. Labe
Date      : 5 October 2020
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import cmocean
import datetime
import scipy.stats as sts

### Directory and time
directorydata = '/Users/zlabe/Desktop/'
directoryfigure = '/Users/zlabe/Desktop/'
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr

### Read in data for pair information
pairinfo = np.genfromtxt(directorydata + 'pairInfoSp19_V1.csv',unpack=True,
                         delimiter=',',skip_header=1)
m1_pairinfo = pairinfo[1,:] # ensemble number
m2_pairinfo = pairinfo[2,:] # ensemble number
trails_pairinfo = pairinfo[3,:]
slope_pairinfo = pairinfo[4,:]
corr_pairinfo = pairinfo[5,:]
r2_pairinfo = pairinfo[6,:]

### Read in data for estimate of similarity of pairs
similar = np.genfromtxt(directorydata + 'estimateSimilarityOfPairs.csv',unpack=True,
                         delimiter=',',skip_header=1)
subject_similar = similar[1,:]
m1_similar = similar[2,:]
m2_similar = similar[3,:]
proc_similar = similar[4,:]
resp_similar = similar[5,:]





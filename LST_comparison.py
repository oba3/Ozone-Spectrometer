# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 10:30:22 2015
Last updated on Tue Jul 30 02:32 2015

@author: O. B. Alam
@email: oalam@haystack.mit.edu
"""
import numpy as np
import matplotlib.pyplot as plt
import shlex
###############################################################################
content     = []    # list for all data
lt          = []    # list for ozone localtime values
mt          = []    # list for ozone month values
vel         = []    # list for ozone velocities
err         = []    # list for ozone errors
plotvel     = []    # list for plotting the weighted averages
plotstd     = []    # list for plotting the errorbars
plotvel2    = []    # list for plotting the weighted averages
plotstd2    = []    # list for plotting the errorbars
###############################################################################
''' returns the weighted average of a data set, given its error set '''
def wavg(data, err):
    num = sum(x*(1/y)*(1/y) for x, y in zip(data, err))
    denom = sum((1/y)*(1/y) for y in err)
    return num/denom

''' returns a normal average of a data set with weight w = 1 '''
def navg(data, err):
    return sum(data)/len(data)
    
''' returns the weighted standard deviation of a data set, given its error set '''
def wstd(data, err):    
    num1 = sum((1/y)*(1/y)*(x-wavg(data, err))*(x-wavg(data, err)) 
                for x, y in zip(data, err))
    num2 = sum((1/y)*(1/y) for y in err)
    num3 = sum((1/y)*(1/y)*(1/y)*(1/y) for y in err)
    return np.sqrt(num1*num2/(num2*num2-num3))
    
''' returns the weighted standard deviation of a data set, given its error set 
    and with weight w = 1. '''
def wstd1(data, err):    
    num1 = sum((x-navg(data, err))*(x-navg(data, err)) for x in data)
    num2 = sum(err)
    num3 = num2
    return np.sqrt(num1*num2/(num2*num2-num3))

''' returns the standard deviation of a data set, given its error set '''
def std(data, err):
    num = sum((x-wavg(data,err))*(x-wavg(data,err)) for x in data)
    denom = len(data) - 1
    return np.sqrt(num/denom)
###############################################################################
''' plots ozone spectrometer velocity measurements vs. localtime '''
def plot_aeer_hourly(lt, vel, err):
    # extract data from file
    with open('vel_vs_localtime.txt') as q: content = q.readlines()
    
    # kill all whitespace and replace with commas
    content = [','.join(shlex.split(x)) for x in content]            
    
    # create separate localtime, velocity, error lists
    for x in content:                                                
        eachRow = x.split(',')
        lt.append(float(eachRow[1]))
        vel.append(float(eachRow[3]))
        err.append(float(eachRow[6]))
        
    # sort all lists by localtime
    lt = np.array(lt)
    vel = np.array(vel)
    err = np.array(err)
    inds = lt.argsort()
    lt = lt[inds].tolist()
    vel = vel[inds].tolist()
    err = err[inds].tolist()
        
    # convert localtime to integers
    lt = [int(x) for x in lt]
    
    # process normal averages and weighted standard deviations
    for i in range(-5,6):
        if i != 5:
            ii = lt.index(i)
            ij  = lt.index(i+1)      
            plotvel.append(navg(vel[ii:ij], err[ii:ij]))
            plotstd.append(wstd(vel[ii:ij], err[ii:ij]))
        else:
            plotvel.append(navg(vel[ij:len(vel)], err[ij:len(vel)]))
            plotstd.append(wstd(vel[ij:len(vel)], err[ij:len(vel)]))
    
    # plot data
    plt.subplot(211)
    plt.plot(range(-5,6), plotvel, '.', label = "Ozone", c = 'blue')
    plt.errorbar(range(-5,6), plotvel, yerr = plotstd, fmt = '.', c = 'blue')
    plt.legend(loc=4) # place the plot legend at the bottom right corner
###############################################################################
plot_aeer_hourly(lt, vel, err)

vel = []
err = []

with open('out_half.txt') as q: vel = q.readlines()
vel = [x.strip('\n') for x in vel]
vel = [x.strip(' ') for x in vel]
vel = [float(x) for x in vel]

with open('out_err_half.txt') as q: err = q.readlines()
err = [x.strip('\n') for x in err]
err = [x.strip(' ') for x in err]
err = [float(x) for x in err]

plt.subplot(212)
plt.plot(np.arange(-5,5.5, 0.5), vel, '.', label = "Fabry-Perot", c = 'red')
plt.errorbar(np.arange(-5,5.5, 0.5), vel, yerr = err, fmt = '.', c= 'red')     
plt.xlim(-6,6) 
plt.legend(loc=4)  
plt.xlabel('Localtime')
plt.ylabel('Velocity (m/s)')
plt.ylim(-30,40)
plt.show()

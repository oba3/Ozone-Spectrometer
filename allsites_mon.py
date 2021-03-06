# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 10:30:22 2015
Last updated on Tue Jul 30 02:321 2015

@author: O. B. Alam
@email: oba3@cornell.edu
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
hour        = []    # list for lidar hours
month       = []    # list for lidar months

plotx = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
plotxhalf = ['J', '', 'F', '', 'M', '', 'A', '', 'M', '', 'J', '', 'J', '', 'A', '', 'S', '', 'O', '', 'N', '', 'D', '']

hays_vel = []
hays_err = []
union_vel = []
union_err = []
chs_vel = []
chs_err = []
###############################################################################
fig = plt.figure(figsize=(10,10))
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
''' plots ozone spectrometer velocity measurements vs. month '''
def plot_aeer_monthly(mt, vel, err):
    with open('vel_vs_month.txt') as q: content = q.readlines()
    content = [','.join(shlex.split(x)) for x in content]
    
    for x in content:
        eachRow = x.split(',')
        mt.append(float(eachRow[1]))
        vel.append(float(eachRow[3]))
        err.append(float(eachRow[6]))
        if(eachRow[8] == 'hays'):
            hays_vel.append(float(eachRow[3]))
            hays_err.append(float(eachRow[6]))
        if(eachRow[8] == 'union'):
            union_vel.append(float(eachRow[3]))
            union_err.append(float(eachRow[6]))        
        if(eachRow[8] == 'chs'):
            chs_vel.append(float(eachRow[3]))
            chs_err.append(float(eachRow[6]))
        
    mt = np.array(mt)
    vel = np.array(vel)
    err = np.array(err)
    
    inds = mt.argsort()
    mt = mt[inds].tolist()
    vel = vel[inds].tolist()
    err = err[inds].tolist()   
    
    mt = [int(x) for x in mt]
    
    # convert days of the year to month number
    for i in xrange(len(mt)):
        if mt[i] == 31:  mt[i] = 2
        if mt[i] == 59:  mt[i] = 3
        if mt[i] == 90:  mt[i] = 4
        if mt[i] == 120: mt[i] = 5
        if mt[i] == 151: mt[i] = 6
        if mt[i] == 181: mt[i] = 7
        if mt[i] == 212: mt[i] = 8
        if mt[i] == 243: mt[i] = 9
        if mt[i] == 273: mt[i] = 10
        if mt[i] == 304: mt[i] = 11
        if mt[i] == 334: mt[i] = 12
    
    for i in range(1,13):
        if i != 12:
            ii = mt.index(i)
            ij  = mt.index(i+1)      
            plotvel.append(navg(vel[ii:ij], err[ii:ij]))
            plotstd.append(wstd(vel[ii:ij], err[ii:ij]))
        else:
            plotvel.append(navg(vel[ij:len(vel)], err[ij:len(vel)]))
            plotstd.append(wstd(vel[ij:len(vel)], err[ij:len(vel)]))

    fig.add_subplot(411)
    plt.xticks(range(1,13), [])
    plt.plot(range(1,13), hays_vel, '.', label = "Haystack", c = 'black')    
    plt.errorbar(range(1,13), hays_vel, yerr = hays_err, fmt = '.', c = 'black')
    plt.legend(loc=4,numpoints=1)
    plt.ylim(-60,40)
    plt.title("Seasonal Variation in Ozone Velocity")       
    plt.xlim(0,13)

    
    fig.add_subplot(412)
    plt.xticks(range(1,13), [])
    plt.plot(range(1,13), union_vel, '.', label = "Union", c = 'black')    
    plt.legend(loc=4,numpoints=1)
    plt.errorbar(range(1,13), union_vel, yerr = union_err, fmt = '.', c = 'black')
    plt.ylim(-60,40)
    plt.xlim(0,13)


    fig.add_subplot(413)
    plt.xticks(range(1,13), [])
    plt.plot(range(1,13), chs_vel, '.', label = "Chelmsford", c = 'black')    
    plt.errorbar(range(1,13), chs_vel, yerr = chs_err, fmt = '.', c = 'black')
    plt.legend(loc=4,numpoints=1)       
    plt.ylim(-60,40)
    plt.ylabel('Meridional Wind Velocity (m/s)')
    plt.xlim(0,13)

       
    fig.add_subplot(414)
    plt.xticks(range(1,13), [])
    plt.plot(range(1,13), plotvel, '.', label = "Ozone average", c = 'black')
    plt.errorbar(range(1,13), plotvel, yerr = plotstd, fmt = '.', c = 'black')
    plt.ylim(-60,40)    
    plt.xlim(0,13)    
    plt.legend(loc=4, numpoints=1) # place the plot legend at the bottom right corner
###############################################################################
plot_aeer_monthly(mt, vel, err)    

vel = []
err = []
min_month = 1
max_month = 13
dt = 0.5

with open('out_halfmon.txt') as q: vel = q.readlines()
vel = [x.strip('\n') for x in vel]
vel = [x.strip(' ') for x in vel]
vel = [float(x) for x in vel]

with open('out_err_halfmon.txt') as q: err = q.readlines()
err = [x.strip('\n') for x in err]
err = [x.strip(' ') for x in err]
err = [float(x) for x in err]
 
plt.xticks(np.arange(min_month, max_month, dt), plotxhalf)
plt.xlabel('Month')
plt.show()
fig.savefig('FINAL_OZONESITESPLOT.eps', format='eps', dpi=1000)

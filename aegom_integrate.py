"""
Created on Wed Jul  1 16:03:32 2015
Last updated Mon Jul 20 15:34 2015

@author: oalam@haystack.mit.edu
"""
import numpy as np

rv      = 9         # dish radius: vertically
rh      = 9         # dish radius: horizontally
f       = 10        # dish focus
f2      = 10.6      # LNBF focus
beam    = 22        # beam correcting factor in gaussian

def run(th):   
    """ setup x, y, z by iterating over a sphere of 
    all possible azimuths and elevations in the sky.
    x is east, y is north, and z is up. """
    sum1 = 0
    sum2 = 0
    for az in range(360):
        for el in range(-90,90):
            x = np.cos(el*np.pi/180)*np.sin(az*np.pi/180)
            y = np.cos(el*np.pi/180)*np.cos(az*np.pi/180)
            z = np.sin(el*np.pi/180)
            
            ''' beam coordinates '''
            xa = x
            ya = y*np.cos(th*np.pi/180) + z*np.sin(th*np.pi/180)
            za = z*np.cos(th*np.pi/180) - y*np.sin(th*np.pi/180)
            ang = np.arctan2(np.sqrt(xa*xa+za*za),ya)*180/np.pi
            
            '''  line from antenna meets dish '''
            a = (x*x+z*z)/(4*f)
            b = y
            c = -f2
            d = (-b + np.sqrt(b*b-4*a*c))/(2*a)
            xd = x*d
            zd = z*d
            r = np.sqrt(((zd-rv)*(zd-rv)/(rv*rv))+xd*xd/(rh*rh))
            b = np.exp(-0.692*ang*ang/(beam*beam))
    
    
            sum1 += b*np.cos(el*np.pi/180)
            if r < 1 : sum2 += b*np.cos(el*np.pi/180)
                
    return sum2/sum1
        
for th in range(0,91):
    print "th " + str(th) + " eff " + str(run(th))

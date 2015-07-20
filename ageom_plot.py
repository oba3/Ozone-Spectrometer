# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 16:03:32 2015
Last updated Mon Jul 20 15:32 2015

@author: oalam@haystack.mit.edu
"""

import shlex
import matplotlib.pyplot as plt

content = []

fig = plt.figure()

# process data
with open('data.txt') as q: content = q.readlines()
content = [','.join(shlex.split(x)) for x in content]
content = [float(x) for x in content]
plt.plot(range(0,91), content, '.')
plt.xlabel('Antenna Orientation (degrees)')
plt.ylabel('Spillover Efficiency')
plt.show()

# save figure as high-quality encapsulated postscript
fig.savefig('lnb.eps', format='eps', dpi=1000)

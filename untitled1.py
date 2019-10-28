# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:10:59 2019

@author: Benjamin
"""
import csv
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
import re
dfs = []
"""
for f in glob.glob('*.csv'):
    df = pd.read_csv(f,skiprows=5)
    df['*.csv'] = os.path.basename(f)
    df['c'] = df['c'].astype(str)
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)
"""

filenames=sorted(glob.glob('*.dat'))
for f in filenames:
    newbozo = pd.read_csv(f,skiprows=5,sep='    ',names='time''strain')
    print (newbozo)
    x=[:,1]
    y=[:,2]
    for row in newbozo:
        x.append((f[0]))
        y.append((f[1]))
        figure=plt.figure ()
       # plot.plt [newbozo]
    plt.plot(x,y, label='')
    plt.xlabel('Time')
    plt.ylabel('Strain')
    plt.title('Creep Curve')
    plt.legend()
    plt.show()
print (filenames)

#filenames=sorted(glob.glob('*.dat'))
#for f in filenames:

"""
import numpy as np


filelist=[glob.glob('*.csv')]


for fname in filelist:
    data=np.loadtxt(f,skiprows=5,delimiter='    ')
    X=data[:,0]
    Y=data[:,1]
    plt.plot(X,Y,':ro')

plt.show()
""" 

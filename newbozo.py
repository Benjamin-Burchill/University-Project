# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:10:59 2019

@author: Benjamin
"""
import pandas as pd
import glob
import matplotlib.pyplot as plt
dfs = {}
"""
for f in glob.glob('*.csv'):
    df = pd.read_csv(f,skiprows=5)
    df['*.csv'] = os.path.basename(f)
    df['c'] = df['c'].astype(str)
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)
"""
filenames=sorted(glob.glob('*.DAT'))#Needs to be upper case on linux windows is case insensitive
figure_counter=1
for f in filenames:
    #dfs[f] = pd.read_csv(f,skiprows=5,engine='python',sep='    ',names='time''strain')
    dfs[f] = pd.read_csv(f,names=['Time','Strain'],engine='python',sep='   ',header=None,skiprows=5)
    
    #x=dfs[f]['Time'] Does the same thing as the two lines below
    newbozo=dfs[f]
    x=newbozo['Time']
    y=newbozo['Strain']
    print (newbozo)
   # for row in newbozo:
        #x.append((f[0]))#What are you doing here ???
    #    y.append((f[1]))
    plt.figure (figure_counter)
    figure_counter+=1
       # plot.plt [newbozo]
    plt.plot(x,y, label='')
    plt.xlabel('Time')
    plt.ylabel('Strain')
    plt.title('Creep Curve')
#    plt.legend() - if the legend is blank why run it?
#print (filenames)
plt.show()



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

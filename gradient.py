# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:10:59 2019

@author: Benjamin
"""
import pandas as pd
import numpy as np
import re
import glob
import matplotlib.pyplot as plt
import math
window_size=20 #The number of points to run our least squares fit on
filenames=sorted(glob.glob('*.DAT'))#Needs to be upper case on Linux. Windows is case insensitive
figure_counter=1
minimum_creep=pd.DataFrame(columns=['Temperature','Stress','Time','Minimum Creep'])
for f in filenames:
#for f in ['1223F85.DAT']: #This line for testing -remove from final
    df = pd.read_csv(f,names=['Time','Strain'],engine='python',sep='   ',header=None,skiprows=5)
    gradients=[] #Create list to put the gradients in
    window_times=[] #List of times to associate with the windows
    min_creep=float('Inf')
    for idx in range(0,len(df.index)-window_size):
      p1=np.polyfit(df.ix[idx:idx+window_size,'Time'],df.ix[idx:idx+window_size,'Strain'],1)#1 is for linear fit
      window_time=np.mean(df.ix[idx:idx+window_size,'Time'])#Save this as we will use it later
      window_times.append(window_time)
      gradients.append(p1[0])#Discard the intercept and take the gradient from our least squares fit
      new_min_creep=min(min_creep,p1[0])
      if (new_min_creep<min_creep):
          min_creep=new_min_creep
          min_creep_time=window_time
    #Stack this away in a data frame too we can print at the end
    nparray=np.vstack((minimum_creep.values,[f[0:4],re.search('(?<=....[DF]).*\.DAT',f).group(0)[:-4],min_creep_time,min_creep]))
    minimum_creep=pd.DataFrame(columns=['Temperature','Stress','Time','MinimumCreep'],data=nparray) 
    minimum_creep.Temperature=minimum_creep.Temperature.astype(float) #Convert to float
    minimum_creep.Stress=minimum_creep.Stress.astype(float) #Convert to float
    minimum_creep.MinimumCreep=minimum_creep.MinimumCreep.astype(float) #Convert to float
    #Put this into a data frame for graphing
    creep_rate=pd.DataFrame(data={'Time':window_times,'Creep Rate':gradients})
    
#Uncomment these graphs for final - but annoying for now.
#    plt.figure (figure_counter)
#    plt.plot(creep_rate['Time'],creep_rate['Creep Rate'])
    #A nice red dot on the graph will show us where the point is so we can 
    #check it looks sensible
#    plt.scatter([min_creep_time],[min_creep],c='r') 
#    plt.xlabel('Time (s)')
 #   plt.xscale('log')
 #   plt.ylabel('Creep Rate')
#    plt.title(f[:-4])#[:-4] to chop off the ugly .DAT at the end
#    figure_counter+=1
#plt.show()
#Make sure it prints everything
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
  print(minimum_creep)
#Read in the Ultimate tensile strength data
uts = pd.read_csv("uts.csv",names=['TempC','UTS'],engine='python',sep=',',header=None,skiprows=1)
abs_zero=273
uts['Temperature']=abs_zero+uts['TempC'] #Add an extra column with temp in K
print(uts)
minimum_creep=pd.merge(minimum_creep,uts[['Temperature','UTS']],on='Temperature')
minimum_creep['NormalisedStress']=minimum_creep['Stress']/minimum_creep['UTS']
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
  print(minimum_creep)
Qc=330.0 #Can make this more complex later but for now use a fixed value
R=8.3144598 #Gas constant
minimum_creep['xdata']=minimum_creep['MinimumCreep']*math.e**(Qc/(R*minimum_creep['Temperature']))
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
  print(minimum_creep)
plt.figure (figure_counter)
plt.scatter(minimum_creep['xdata'],minimum_creep['NormalisedStress'],c='r') 
plt.xlabel('x')
#plt.xlim([minimum_creep['xdata'].min,minimum_creep['xdata'].max])
plt.ylabel('y')
#plt.xscale('log')
#plt.title(f[:-4])#[:-4] to chop off the ugly .DAT at the end
plt.show()

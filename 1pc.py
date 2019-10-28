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
filenames=sorted(glob.glob('*.DAT'))#Needs to be upper case on Linux. Windows is case insensitive
figure_counter=1
strain_rate=0.01 #1 per cent
df_outs={}
df_out=pd.DataFrame(columns=['Temperature','Stress','Time','CreepRate','PreviousCreep'])
temps=set()
for f in filenames:
#for f in ['1223F85.DAT']: #This line for testing -remove from final
    temps.add(f[0:4])
    df = pd.read_csv(f,names=['Time','Strain'],engine='python',sep='   ',header=None,skiprows=5)
    this_strain=0.0 #Starting from zero
    last_strain=0.0
    for idx in range(0,len(df.index)):
      last_strain=this_strain
      if (this_strain<=df.ix[idx,'Strain']):
          this_strain=df.ix[idx,'Strain']
          this_time=df.ix[idx,'Time']
      if(this_strain>=strain_rate):
          break
    #Stack this away in a data frame too we can print at the end
    nparray=np.vstack((df_out.values,[f[0:4], \
                       re.search('(?<=....[DF]).*\.DAT',f).group(0)[:-4], \
                       this_time,this_strain,last_strain]))
    df_out=pd.DataFrame(columns=['Temperature','Stress','Time','CreepRate','PreviousCreep'],data=nparray) 
    df_out.Temperature=df_out.Temperature.astype(float) #Convert to float
    df_out.Stress=df_out.Stress.astype(float) #Convert to float
    df_out.Time=df_out.Time.astype(float) #Convert to float
    df_out.CreepRate=df_out.CreepRate.astype(float) #Convert to float
    df_out.PreviousCreep=df_out.PreviousCreep.astype(float) #Convert to float
#Read in the Ultimate tensile strength data
uts = pd.read_csv("uts.csv",names=['TempC','UTS'],engine='python',sep=',',header=None,skiprows=1)
abs_zero=273
uts['Temperature']=abs_zero+uts['TempC'] #Add an extra column with temp in K
print(uts)
df_out=pd.merge(df_out,uts[['Temperature','UTS']],on='Temperature')
df_out['NormalisedStress']=df_out['Stress']/df_out['UTS']
Qc=330.0 #Can make this more complex later but for now use a fixed value
R=8.3144598 #Gas constant
df_out['xdata']=df_out['Time']*math.e**(-Qc/(R*df_out['Temperature']))
for temp in temps:
    print(temp)
    f_temp=float(temp)
    df_outs[temp]=df_out.loc[df_out['Temperature'] == f_temp]
#    plt.scatter(df_outs[temp]['xdata'],df_outs[temp]['NormalisedStress'],label=str(temp)+'K') 
    plt.scatter(df_outs[temp]['Time'],df_outs[temp]['NormalisedStress'],label=str(temp)+'K') 

    
#Make sure it prints everything
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
  print(df_out)
plt.title(str(strain_rate*100)+'% Creep Rates')
plt.xlabel('Time')
plt.ylabel('Normalised Stress')
plt.legend(loc='upper right')
#plt.xlim([df_out['xdata'].min,df_out['xdata'].max])
plt.xscale('log')
plt.show()
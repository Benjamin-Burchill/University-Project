#!/usr/bin/python3
# Ben Burchill 3rd Year project 2019
import os,re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#==============================================
#===Load the data into a dictionary============
#==============================================
dfs={}      #Big collection of *all* the data
   
#Assume that our script is in the same folder as the .dat files
#Get a listing of all the files in this current folder
_files=os.listdir(os.getcwd())
__files=[] #List we will put a score in for sorting
#Loop through all the files in this folder
for _file in _files:
  #But only pick the ones that match this regular expression so we don't try to process non-data files
  if (re.match('....[DF].*\.DAT',_file)):
    temp=int(_file[0:4]) #Temperature is first four letters of file name
    #We need a regex here again as the stress might be 3 or 4 digits
    stress=re.search('(?<=....[DF]).*\.DAT',_file).group(0)[:-4]
    sortorder=1000*temp+int(stress) #Create a score for sorting and remove the .DAT from the end
    __files.append([sortorder,_file]) #Put in the list with the filename
_files=[] #Clear down the old list as we will now overwrite it and
#replace with our cleaned and sorted list
for __file in sorted(__files):
  _files.append(__file[1]) #We are just taking the filename now and discard the score
#==============================================
#Create a set of temperatures as we are going to make a plot with 
#the failures for each temperature. 
temps=set()
for _file in _files:
  temps.add(_file[0:4])
#==============================================
#Loop through all the data files in this folder
for _file in _files:
  #Load the data into our dictionary for later plotting and processing
  #We need to use the python engine as we are using a multiple character delimiter
  #There are either 3 or 4 spaces between the columns
  #First five rows have header information in them so can be skipped.
  #No actual headings in the file so we create them here.
  dfs[_file]=pd.read_csv(_file,names=['Time','Strain'],engine='python',sep='   ',header=None,skiprows=5)
#==============================================
#Now put the rupture points into a collection organised by temperature
ruptures={} #The rupture collection
#First we need to make empty data frames so we can add to these
for temp in sorted(temps):
  ruptures[temp]=pd.DataFrame(columns=['Time','Stress','Temperature'],dtype=float) #Data frame for failures
#Now run through our big data collection and pull out all the rupture points
for _file in _files: 
  temp=_file[0:4] #First four characters of the filename are the temperature
  stress=re.search('(?<=....[DF]).*\.DAT',_file).group(0)[:-4]
  #Stack the existing tempature data with the rupture point we have pulled out
  #-1 to make sure we get the last record and the rupture point
  nparray=np.vstack((ruptures[temp].values,[dfs[_file][-1:]['Time'],int(stress),temp]))
  ruptures[temp]=pd.DataFrame(columns=['Time','Stress','Temperature'],data=nparray,dtype=float) #Data frame for failures
for temp in sorted(temps):
  ruptures[temp]=ruptures[temp].sort_values('Time')
  plt.figure(1)
  plt.plot(ruptures[temp]['Time'],ruptures[temp]['Stress'],label=temp+'K')
  plt.figure(2)
  plt.scatter(ruptures[temp]['Time'],ruptures[temp]['Stress'],label=temp+'K')
print(ruptures)
for fig in [1,2]:
  plt.figure(fig)
  plt.xscale('log')
  plt.ylabel('Stress MPa')
  plt.xlabel('Time (s)')
  plt.legend(loc='upper right')
  plt.title('Rupture Points by Temperature')
#===========================================================================
uts = pd.read_csv("uts.csv",names=['TempC','UTS'],engine='python',sep=',',header=None,skiprows=1)
abs_zero=273
uts['Temperature']=abs_zero+uts['TempC'] #Add an extra column with temp in K
print(uts)
all_ruptures=pd.concat(ruptures,axis=0)
all_ruptures=pd.merge(all_ruptures,uts[['Temperature','UTS']],on='Temperature')
all_ruptures['NormalisedStress']=all_ruptures['Stress']/all_ruptures['UTS']
#Qc=330.0 #Can make this more complex later but for now use a fixed value
Qc=200.0 #Can make this more complex later but for now use a fixed value
R=8.3144598 #Gas constant
all_ruptures['xdata']=all_ruptures['Time']*math.e**(-Qc/(R*all_ruptures['Temperature'])) 
#Take logs for the plot
all_ruptures['xdata']=np.log(all_ruptures['xdata'])
all_ruptures['NormalisedStress']=np.log(-np.log(all_ruptures['NormalisedStress']))
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
  print(all_ruptures)
plt.figure(3)
plt.scatter(all_ruptures['xdata'],all_ruptures['NormalisedStress'])
#plt.xscale('log')
#plt.yscale('log')
plt.ylabel('Normalised Stress')
plt.xlabel('xdata')
plt.title('Wilshire Plot')



plt.show()

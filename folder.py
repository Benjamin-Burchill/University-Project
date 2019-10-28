#!/usr/bin/python3
# Ben Burchill 3rd Year project 2019
import os,re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
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
#Loop through all the data files in this folder
for _file in _files:
  #Load the data into our dictionary for later plotting and processing
  #We need to use the python engine as we are using a multiple character delimiter
  #There are either 3 or 4 spaces between the columns
  #First five rows have header information in them so can be skipped.
  #No actual headings in the file so we create them here.
  dfs[_file]=pd.read_csv(_file,names=['Time','Strain'],engine='python',sep='   ',header=None,skiprows=5)
#==============================================
#Create a set of temperatures and stresses series of plots per temp 
#and stress
temps=set()
stresses=set()
for _file in _files:
  temps.add(_file[0:4])
  stresses.add(re.search('(?<=....[DF]).*\.DAT',_file).group(0)[:-4])
#==============================================
for _file in _files: 
  temp_figure_count=0
  for temp in temps:
    temp_figure_count += 1   
    if (re.match(temp+'[DF].*\.DAT',_file)):
      plt.figure(temp_figure_count)
      stress=re.search('(?<=....[DF]).*\.DAT',_file).group(0)[:-4]
      plt.plot(dfs[_file]['Time'],dfs[_file]['Strain'],label=stress+'MPa')
      plt.title('Temperature '+ temp + 'K')
  stress_figure_count = len(temps) #stress figures come after the temp ones
  for stress in stresses:
    stress_figure_count+=1
    if(re.match('....[DF]'+stress,_file)):
      plt.figure(stress_figure_count)
      plt.plot(dfs[_file]['Time'],dfs[_file]['Strain'],label=_file[0:4]+'K')
      plt.title('Stress '+ stress + 'MPa')
#================Filter Graphs=========================================================
filter_figure_count = len(temps)+len(stresses)+1 #stress figures come after the temp ones
for _file in ['1123F190.DAT','1223F200.DAT']: #Some hand selected plots to test filters with
  for temp in temps:
    if (re.match(temp+'[DF].*\.DAT',_file)):
      for stress in stresses:
        if(re.match('....[DF]'+stress,_file)):
          plt.figure(filter_figure_count)
          stress=re.search('(?<=....[DF]).*\.DAT',_file)
          sgf=savgol_filter(dfs[_file]['Strain'],11,4)
          plt.plot(dfs[_file]['Time'],dfs[_file]['Strain'],label=_file[:-4])
          plt.plot(dfs[_file]['Time'],sgf,label='Savgold Filter')
          plt.title('Savgold Filter '+ _file[:-4])
  filter_figure_count+=1
for fig in range(1,filter_figure_count):
  plt.figure(fig)
  plt.ylabel('Strain %')
  plt.xlabel('Time (s)')
  plt.xscale('log')
  plt.legend(loc='upper left')
plt.show()
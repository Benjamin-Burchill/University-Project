#!/usr/bin/python3
import pandas as pd, numpy as np
mydf = pd.DataFrame(columns=['Foo','Bar','Baz'],data=[[1.1,1.1, 1.1]],dtype=float) #Original data frame
print('Original Data Frame') 
print(mydf) 
arow = [2.2, 2.2, 2.2] #Row 2
mynparray = np.vstack((mydf.values,arow)) #as a numpy array stuck together
mydf = pd.DataFrame(columns=['Foo','Bar','Baz'],data=mynparray,dtype=float) #New dataframe with our data
print('New Data Frame') 
print(mydf)
arow = [3.3, 3.3, 3.3] #Row 3
mynparray = np.vstack((mydf.values,arow)) #as a numpy array stuck together
mydf = pd.DataFrame(columns=['Foo','Bar','Baz'],data=mynparray,dtype=float) #New dataframe with our data
print('New Data Frame') 
print(mydf)

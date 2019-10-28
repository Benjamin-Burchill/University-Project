#!/usr/bin/python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as ss
#import scipy
x=np.arange(1,100,0.1)
mu=500
sigma=500
y=np.random.normal(mu,sigma,len(x))
df=pd.DataFrame({'x':x,'y':y},columns=['x','y'])
df['y']=df.x*df.x+df.y
#The unfiltered data
plt.plot(df['x'],df['y'],label='y')
#b,a=ss.butter(4,100,'low',analog=True)
b,a=ss.butter(2,0.005,'lowpass',analog=True)
df['y_filter']=ss.lfilter(b,a,df['y'])
plt.plot(df['x'],df['y_filter'],label='y_filter')
plt.show()
print(df)

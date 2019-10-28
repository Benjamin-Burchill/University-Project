#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
dfs={}
dfs[0]=pd.read_csv('test.csv')
dfs[1]=pd.read_csv('test2.csv')
print(dfs[0])
print(dfs[1])
#print data.mean()
plt.plot(dfs[0]['foo'],dfs[0]['bar'],'r--',dfs[1]['baz'],dfs[1]['quux'],'g--')
plt.xlabel('foo')
plt.ylabel('bar')
plt.show()

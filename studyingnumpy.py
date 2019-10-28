# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 17:09:32 2019

@author: Benjamin
"""
import numpy as np
import pandas as pd
from numpy import genfromtxt
import glob
import matplotlib.pyplot
filenames=sorted(glob.glob('*.dat'))
for f in filenames:
    print(f)
    def readData():
        with open("filenames", "r") as MyFile:
           for i in range(5):
                next(myFile) # skip line
           myList = [lines.split() for lines in myFile]
        return myList
    data= np.loadtxt(fname=f,delimiter=',')
""" fig=matplotlib.pyplot.figure(figzsize(10.0,3.0))
    axes1 = fig.add_subplot(1, 3, 1)
    axes2 = fig.add_subplot(1, 3, 2)
    axes3 = fig.add_subplot(1, 3, 3)

    axes1.set_ylabel('average')
    axes1.plot(numpy.mean(data, axis=0))

    axes2.set_ylabel('max')
    axes2.plot(numpy.max(data, axis=0))

    axes3.set_ylabel('min')
    axes3.plot(numpy.min(data, axis=0))

    fig.tight_layout()
    matplotlib.pyplot.show()"""
#mydata=genfromtext('1098f150',',')
#newarray=mydata.diff
#print(glob.glob('*.dat'))
'''
Created on 22-Apr-2017

@author: ManiRao
'''
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)

x = np.random.normal(0,5,1000)
numBins = 500
ax.hist(x,numBins,color='blue',alpha=0.2)
plt.xlim([0,5])
plt.show()


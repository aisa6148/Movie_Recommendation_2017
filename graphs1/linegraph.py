'''
Created on 21-Apr-2017

@author: ManiRao
'''
import numpy as np
import matplotlib.pyplot as plt
import pylab

# Come up with x and y
x = np.arange(0, 4, 0.1)
y = np.sin(x)
# Just print x and y for fun
print (x)
print (y)
# plot the x and y and you are supposed to see a sine curve
plt.plot(x, y)
# without the line below, the figure won't show
pylab.show()
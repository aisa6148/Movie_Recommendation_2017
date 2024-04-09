'''
Created on 23-Apr-2017

@author: Karthik_pc
'''
'''import matplotlib.pyplot as plt
import numpy as np
from numpy.core.multiarray import arange
import random
import BasicModules

def histogram(xvalues=[], yvalues=[], labels=[], xlimit=10, ylimit=10):
    fig = plt.figure()
    
    plt.bar(left=xvalues, height=yvalues)
    plt.xlabel('Users')
    plt.xticks(xvalues,labels)
    plt.xlim([-0.5, xlimit])
    plt.ylim([0, ylimit])
    plt.show() 

#x = np.random.normal(0,5,1000)
#numBins = 50
#ax.hist(x,numBins,color='blue',alpha=0.2)
#plt.xlim([0,5])

def scatter(xvalues=[], yvalues=[], n=20, ax=None):
    area=np.pi*(4**2)
    ax.scatter(xvalues[:n], yvalues[:n], color='green',s=area,edgecolor='none', alpha=0.5)
    area=np.pi*(2**2)
    ax.scatter(xvalues[n:], yvalues[n:], color='red',s=area,edgecolor='none', alpha=0.5)
    xmax=max(xvalues)
    plt.xlim([0,xmax])
    plt.xlabel('Number of users')
    plt.ylabel('Weighted movie rating')
    plt.xticks(arange(0, xmax, 2))
    
    ## left panel
    
    #ax1.scatter(x,y,color='blue',s=5,edgecolor='none')
    #ax1.set_aspect(1./ax1.get_data_ratio()) # make axes square
    
#scatter([1,2,3,4],[5,6,7,8],n=2)
def collectScatter():
    f, axs= plt.subplots(1, len(BasicModules.scatter_list))
    
    i=0
    for ax in axs.flat:
        temp=BasicModules.scatter_list[i]
        scatter(xvalues=temp[0], yvalues=temp[1], n=temp[2], ax=ax)
        i=i+1
        
    plt.show()

def pie(values=[], labels=[], ax=None, title=''):
    colors = ['pink', 'yellow', 'green', 'blue', 'red', 'cyan', 'violet', 'orange', 'beige', 'grey']
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.set_title(title)
    ax.axis('equal')
    

def collectPies(values, labels, titles):    
    f, axs= plt.subplots(1, len(values))
    i=0
    for ax in axs.flat:        
        pie(values=values[i], labels=labels[i], ax=ax, title=titles[i])
        i=i+1    
    plt.show()
    
def bar(xvalues=[], yvalues=[], labels=[], legend=[]):
    if len(xvalues) == 0:
        xvalues=arange(0,len(yvalues))
    colors = ['pink', 'yellow', 'green', 'blue', 'red', 'cyan', 'violet', 'orange', 'beige', 'grey', 'magenta']
    bottom=[]
    plts=[]
    for i in range(len(yvalues)):
        bottom.append(0)
    for i in range(len(yvalues[0])):                       
        values=[item[i] for item in yvalues]        
        plts.append(plt.bar(arange(len(yvalues)), values, bottom=bottom, color=colors[i%len(colors)]))
        for j in range(len(values)):            
            #bottom[j]+=yvalues[i][j]
            bottom[j]+=yvalues[j][i]
    plt.xlabel('Movie')
    plt.ylabel('Cumulative Score')
    
    plt.legend(plts, legend)
    plt.xticks(xvalues, tuple(labels))
    plt.show()

#values=[[4,6,3,5,8,10,12,3,6],[4,6,3,5,8,10,12,3,6,13]]
#labels=[['Comedy','Horror','Drama','Crime','Action','Film-Noir','Adventure','Documentary','Sci-fi'], ['Comedy','Horror','Drama','Crime','Action','Film-Noir','Adventure','Documentary','Sci-fi','One']]   
#collectPies(values, labels, titles=['Old', 'New'])
'''
'''xvalues=[1,2,3,4,5,6]
yvalues=[[2,3,4,2,3,4],[4,3,2,4,3,2]]
bar(yvalues=yvalues)
'''
'''
values=[4,6,3,5,8,10,12,3,6]
labels=['Comedy','Horror','Drama','Crime','Action','Film-Noir','Adventure','Documentary','Sci-fi']
pie(values=values, labels=labels)
'''
'''
xvalues=arange(6)
yvalues=[]
for x in range(6):
    yvalues.append(random.randint(0,10))
histogram(xvalues, yvalues,[123, 1212, 42, 6, 785, 12])
'''

'''
Created on 22-Apr-2017

@author: ManiRao
'''
import numpy as np
import matplotlib.pyplot as plt


n_groups = 5

means_person1 = (20, 35, 30, 35, 27)
std_means1 = (2, 3, 4, 1, 2)

means_person2 = (25, 32, 34, 20, 25)
std_means2 = (3, 5, 2, 3, 3)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index, means_person1, bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=std_means1,
                 error_kw=error_config,
                 label='Person 1')

rects2 = plt.bar(index + bar_width, means_person2, bar_width,
                 alpha=opacity,
                 color='r',
                 yerr=std_means2,
                 error_kw=error_config,
                 label='People2/Others')

plt.xlabel('People')
plt.ylabel('Scores')
plt.title('Scores by user1 against users')
plt.xticks(index + bar_width / 2, ('A', 'B', 'C', 'D', 'E'))
plt.legend()

plt.tight_layout()
plt.show()

def autolabel(rects):
    
    #Attach a text label above each bar displaying its height
    
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.show()
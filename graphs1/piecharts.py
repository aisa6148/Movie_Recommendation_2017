'''
Created on 21-Apr-2017

@author: ManiRao
'''
import matplotlib.pyplot as plt
 
# Data to plot
labels = 'Horror', 'Comedy', 'Action', 'Thriller'
sizes = [215, 130, 245, 210]
colors = ['pink', 'yellow', 'green', 'blue']
explode = (0.1, 0, 0, 0)  # explode 1st slice
 
# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.show()
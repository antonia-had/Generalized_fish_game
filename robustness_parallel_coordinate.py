import matplotlib
from matplotlib import pyplot as plt
from matplotlib import patheffects as pe
import numpy as np
plt.style.use('ggplot')

fig = plt.figure(figsize=(18,9)) # create the figure
ax = fig.add_subplot(1, 1 , 1)    

robustness = np.loadtxt('./Robustness.txt',delimiter=' ')*100

objs_labels = ['Net present\nvalue (NPV) > 1500', 
               'Prey population\ndeficit < 0.2', 
               'Longest duration\nof low harvest < 5', 
               'Worst harvest\ninstance > 50',
               'Variance of harvest < 30000',
               'Duration of predator\npopulation collapse < 1']


cmap = matplotlib.cm.get_cmap("Purples")
robustness = robustness[robustness[:,-1].argsort()]
normalized_color = robustness[:,-1]/np.max(robustness[:,-1])-np.min(robustness[:,-1])
for i in range(len(robustness[:,0])):
    ys = robustness[i,:]
    xs = range(len(ys))
    ax.plot(xs[0:6], ys[0:6], c=cmap(normalized_color[i]), linewidth=2) 
    
# Highlight specific solutions
ys = robustness[np.argmax(robustness[:,0]),:] # Most robust in NPV
xs = range(len(ys))
l1=ax.plot(xs[0:6], ys[0:6], c=cmap(normalized_color[np.argmax(robustness[:,0])]), linewidth=3, label='Most robust in NPV', path_effects=[pe.Stroke(linewidth=6, foreground='darkgoldenrod'), pe.Normal()])

ys = robustness[np.argmax(robustness[:,-1]),:] # Most robust in all criteria
xs = range(len(ys))
l2=ax.plot(xs[0:6], ys[0:6], c=cmap(normalized_color[np.argmax(robustness[:,5])]), linewidth=3, label='Most robust across criteria', path_effects=[pe.Stroke(linewidth=6, foreground='gold'), pe.Normal()])

sm = matplotlib.cm.ScalarMappable(cmap=cmap)
sm.set_array([robustness[:,-1].min(),robustness[:,-1].max()])
cbar = fig.colorbar(sm)
cbar.ax.set_ylabel("Percentage of SOW where all criteria are met (%)")
ax.set_ylabel("Percentage of SOW where each criterion is met (%)", size= 12)
ax.set_yticks(np.arange(0,110,20))
ax.set_xticks([0,1,2,3,4,5])
ax.set_xticklabels(objs_labels)
ax.legend()
plt.savefig('robustness_parallel_coordinate.png')




import matplotlib
from matplotlib import pyplot as plt
import numpy as np
plt.style.use('ggplot')
plt.switch_backend('agg')
plt.ioff()

fig = plt.figure(figsize=(18,9)) # create the figure
ax = fig.add_subplot(1, 1, 1)    # make axes to plot on

reference = np.loadtxt('./Generalized.reference',delimiter=' ') # Read in all solutions
reference = -reference

objs_labels = ['Net present\nvalue (NPV)', 
               'Prey population deficit', 
               'Longest duration\nof low harvest', 
               'Worst harvest instance',
               'Duration of predator\npopulation collapse'] # Constraint (always 0)

# Normalization across objectives
mins = reference.min(axis=0)
maxs = reference.max(axis=0)
norm_reference = reference.copy()
for i in range(4):
    mm = reference[:,i].min()
    mx = reference[:,i].max()
    if mm!=mx:
        norm_reference[:,i] = (reference[:,i] - mm) / (mx - mm)
    else:
        norm_reference[:,i] = 1

cmap = matplotlib.cm.get_cmap("Blues")

## Plot all solutions
for i in range(len(norm_reference[:,0])):
    ys = np.append(norm_reference[i,:], 1.0)
    xs = range(len(ys))
    ax.plot(xs, ys, c=cmap(ys[0]), linewidth=2)

#Colorbar
sm = matplotlib.cm.ScalarMappable(cmap=cmap)
sm.set_array([reference[:,0].min(),reference[:,0].max()])
cbar = fig.colorbar(sm)
cbar.ax.set_ylabel("\nNet present value (NPV)")

# Tick values
minvalues = ["{0:.3f}".format(mins[0]), "{0:.3f}".format(-mins[1]),str(-mins[2]), str(mins[3]), str(0)]
maxvalues = ["{0:.2f}".format(maxs[0]), "{0:.3f}".format(-maxs[1]),str(-maxs[2]), "{0:.2f}".format(maxs[3]), str(0) ]

ax.set_ylabel("Preference ->", size= 12)
ax.set_yticks([])
ax.set_xticks([0,1,2,3,4])
ax.set_xticklabels([minvalues[i]+'\n'+objs_labels[i] for i in range(len(objs_labels))])
#make a twin axis for toplabels
ax1 = ax.twiny()
ax1.set_yticks([])
ax1.set_xticks([0,1,2,3,4])
ax1.set_xticklabels([maxvalues[i] for i in range(len(maxs))])
plt.savefig('Objectives_parallel_axis.svg')
plt.savefig('Objectives_parallel_axis.png')
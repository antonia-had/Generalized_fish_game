import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import os
plt.style.use('ggplot')
plt.switch_backend('agg')
plt.ioff()

objs_labels = ['Net present\nvalue (NPV)', 
               'Prey population deficit', 
               'Longest duration\nof low harvest', 
               'Worst harvest instance',
               'Variance of harvest',
               'Duration of predator\npopulation collapse']

nSamples=4000 # Number of SOW
nObjs=5
nCnstr = 1
numPts = (len(os.listdir('./Generalized/resim_objs'))) # Get number of solutions on pareto front

def reformatData(method, SOW):
    objs = np.zeros([len(SOW), numPts, nObjs])
    cnstr = np.zeros([len(SOW), numPts])
    for j in range(numPts):
        objectives = './Generalized/resim_objs/' + method + '_objs_' + str(int(j)) + '.txt'
        constraints = './Generalized/resim_cnstr/' + method + '_cnstr_' + str(int(j)) + '.txt'
        with open(objectives) as fp:
            for i, line in enumerate(fp):
                for k in range(len(SOW)):
                    if i == SOW[k]:
                        data = line.split()
                        objs[k,j,:] = data
                        if objs[k,j,0]>0 or objs[k,j,3]>0:
                            objs[k,j,:] = 0
        with open(constraints) as fp:
            for i, line in enumerate(fp):
                for k in range(len(SOW)):
                    if i == SOW[k]:
                        cnstr[k,j] = line
    return objs, cnstr

reference = np.loadtxt('./Generalized.reference',delimiter=' ')
optimized_alternative1 = np.loadtxt('./Reoptimized_1540.reference',delimiter=' ')
optimized_alternative2 = np.loadtxt('./Reoptimized_2832.reference',delimiter=' ')
optimized_alternative3 = np.loadtxt('./Reoptimized_1253.reference',delimiter=' ')
objs, cnstr = reformatData('Previous_Prey', [1540, 2832, 1253])

reference = -reference
optimized_alternative1 = -optimized_alternative1
optimized_alternative2 = -optimized_alternative2
optimized_alternative3 = -optimized_alternative3
objs = -objs
cnstr = -cnstr

norm_reference = reference.copy()
norm_alternative1 = optimized_alternative1.copy()
norm_alternative2 = optimized_alternative2.copy()
norm_alternative3 = optimized_alternative3.copy()
norm_objs = objs.copy()

# Normalize pairs of sets for each SOW
mins1 = np.zeros([2,nObjs])
maxs1 = np.zeros([2,nObjs])
mins1[0] = optimized_alternative1.min(axis=0)
maxs1[0] = optimized_alternative1.max(axis=0)
mins1[1] = objs[:,:,:].min(axis=1)[0]
maxs1[1] = objs[:,:,:].max(axis=1)[0]

mins2 = np.zeros([2,nObjs])
maxs2 = np.zeros([2,nObjs])
mins2[0] = optimized_alternative2.min(axis=0)
maxs2[0] = optimized_alternative2.max(axis=0)
mins2[1] = objs[:,:,:].min(axis=1)[1]
maxs2[1] = objs[:,:,:].max(axis=1)[1]

mins3 = np.zeros([2,nObjs])
maxs3 = np.zeros([2,nObjs])
mins3[0] = optimized_alternative3.min(axis=0)
maxs3[0] = optimized_alternative3.max(axis=0)
mins3[1] = objs[:,:,:].min(axis=1)[2]
maxs3[1] = objs[:,:,:].max(axis=1)[2]

for i in range(nObjs):
    norm_alternative1[:,i] = (optimized_alternative1[:,i] - np.min(mins1[:,i])) / (np.max(maxs1[:,i]) - np.min(mins1[:,i]))
    norm_alternative2[:,i] = (optimized_alternative2[:,i] - np.min(mins2[:,i])) / (np.max(maxs2[:,i]) - np.min(mins2[:,i]))
    norm_alternative3[:,i] = (optimized_alternative3[:,i] - np.min(mins3[:,i])) / (np.max(maxs3[:,i]) - np.min(mins3[:,i]))
    norm_objs[0,:,i] = (objs[0,:,i] - np.min(mins1[:,i])) / (np.max(maxs1[:,i]) - np.min(mins1[:,i]))
    norm_objs[1,:,i] = (objs[1,:,i] - np.min(mins2[:,i])) / (np.max(maxs2[:,i]) - np.min(mins2[:,i]))
    norm_objs[2,:,i] = (objs[2,:,i] - np.min(mins3[:,i])) / (np.max(maxs3[:,i]) - np.min(mins3[:,i]))

if np.max(cnstr[0])==np.min(cnstr[0]):
    norm_cnstr1 = np.zeros(len(cnstr[0,:]))
else:
    norm_cnstr1 = (cnstr[0]-np.min(cnstr[0]))/(np.max(cnstr[0])-np.min(cnstr[0]))
if np.max(cnstr[1])==np.min(cnstr[1]):   
    norm_cnstr2 = np.zeros(len(cnstr[0,:]))
else:
    norm_cnstr2 = (cnstr[1]-np.min(cnstr[1]))/(np.max(cnstr[1])-np.min(cnstr[1]))
if np.max(cnstr[2])==np.min(cnstr[2]):
    norm_cnstr3 = np.zeros(len(cnstr[0,:]))
else:
    norm_cnstr3 = (cnstr[2]-np.min(cnstr[2]))/(np.max(cnstr[2])-np.min(cnstr[2]))

# Define colormap for each SOW
cmap1 = matplotlib.cm.get_cmap("Oranges")
cmap2 = matplotlib.cm.get_cmap("Greens")
cmap3 = matplotlib.cm.get_cmap("Reds")

fig = plt.figure(figsize=(18,9)) # create the figure
#First SOW
ax1 = fig.add_subplot(3, 1, 1)    # make axes to plot on
for i in range(len(norm_objs[0,:,:])):
    ys = np.append(norm_objs[0,i,:],norm_cnstr1[i])
    xs = range(len(ys))
    ax1.plot(xs, ys, c='grey', linewidth=2) 
    
for i in range(len(norm_alternative1[:,0])):
    ys = np.append(norm_alternative1[i,:], 1.0)
    xs = range(len(ys))
    ax1.plot(xs, ys, c=cmap1(ys[0]), linewidth=2)

sm1 = matplotlib.cm.ScalarMappable(cmap=cmap1)
sm1.set_array([np.min(mins1[:,0]),np.max(maxs1[:,0])])
cbar1 = fig.colorbar(sm1)

#Second SOW
ax2 = fig.add_subplot(3, 1, 2)    # make axes to plot on   
for i in range(len(norm_objs[1,:,:])):
    ys = np.append(norm_objs[1,i,:],norm_cnstr2[i])
    xs = range(len(ys))
    ax2.plot(xs, ys, c='grey', linewidth=2) 
    
for i in range(len(norm_alternative2[:,0])):
    ys = np.append(norm_alternative2[i,:], 1.0)
    xs = range(len(ys))
    ax2.plot(xs, ys, c=cmap2(ys[0]), linewidth=2) 

sm2 = matplotlib.cm.ScalarMappable(cmap=cmap2)
sm2.set_array([np.min(mins2[:,0]),np.max(maxs2[:,0])])
cbar2 = fig.colorbar(sm2)

#Third SOW
ax3 = fig.add_subplot(3, 1, 3)    # make axes to plot on   
for i in range(len(norm_objs[2,:,:])):
    ys = np.append(norm_objs[2,i,:],norm_cnstr3[i])
    xs = range(len(ys))
    ax3.plot(xs, ys, c='grey', linewidth=2) 
    
for i in range(len(norm_alternative3[:,0])):
    ys = np.append(norm_alternative3[i,:], 1.0)
    xs = range(len(ys))
    ax3.plot(xs, ys, c=cmap3(ys[0]), linewidth=2) 

sm3 = matplotlib.cm.ScalarMappable(cmap=cmap3)
sm3.set_array([np.min(mins3[:,0]),np.max(maxs3[:,0])])
cbar3 = fig.colorbar(sm3)

plt.subplots_adjust(hspace = 0.3)
ax1.set_yticks([])
ax2.set_yticks([])
ax3.set_yticks([])
ax1.set_xticks([0,1,2,3,4])
ax2.set_xticks([0,1,2,3,4])
ax3.set_xticks([0,1,2,3,4])

# Tick values
minvalues = ["{0:.2f}".format(np.min(mins1, axis=0)[0]), 
             "{0:.2f}".format(-np.min(mins1, axis=0)[1]), 
             str(-np.min(mins1, axis=0)[2]), 
             "{0:.2f}".format(np.min(mins1, axis=0)[3]), 
             "{0:.2f}".format(-np.min(mins1, axis=0)[4]), 
             str(-np.min(cnstr[0]))]
maxvalues = ["{0:.2f}".format(np.max(maxs1, axis=0)[0]), 
             "{0:.2f}".format(-np.max(maxs1, axis=0)[1]), 
             str(-np.max(maxs1, axis=0)[2]), 
             "{0:.2f}".format(np.max(maxs1, axis=0)[3]), 
             "{0:.2f}".format(-np.max(maxs1, axis=0)[4]),
             str(-np.max(cnstr[0]))]
#make a twin axis for toplabels
ax1t = ax1.twiny()
ax1t.set_yticks([])
ax1t.set_xticks([0,1,2,3,4])
ax1.set_xticklabels(minvalues)
ax1t.set_xticklabels(maxvalues)

minvalues = ["{0:.2f}".format(np.min(mins2, axis=0)[0]), 
             "{0:.2f}".format(-np.min(mins2, axis=0)[1]), 
             str(-np.min(mins2, axis=0)[2]), 
             "{0:.2f}".format(np.min(mins2, axis=0)[3]), 
             "{0:.2f}".format(-np.min(mins2, axis=0)[4]), 
             str(-np.min(cnstr[1]))]
maxvalues = ["{0:.2f}".format(np.max(maxs2, axis=0)[0]), 
             "{0:.2f}".format(-np.max(maxs2, axis=0)[1]), 
             str(-np.max(maxs2, axis=0)[2]), 
             "{0:.2f}".format(np.max(maxs2, axis=0)[3]),
             "{0:.2f}".format(-np.max(maxs2, axis=0)[4]),
             str(-np.max(cnstr[1]))]
#make a twin axis for toplabels
ax2t = ax2.twiny()
ax2t.set_yticks([])
ax2t.set_xticks([0,1,2,3,4])
ax2.set_xticklabels(minvalues)
ax2t.set_xticklabels(maxvalues)

minvalues = ["{0:.2f}".format(np.min(mins3, axis=0)[0]), 
             "{0:.2f}".format(-np.min(mins3, axis=0)[1]), 
             str(-np.min(mins3, axis=0)[2]), 
             "{0:.2f}".format(np.min(mins3, axis=0)[3]),
             "{0:.2f}".format(-np.min(mins3, axis=0)[4]), 
             str(-np.min(cnstr[2]))]
maxvalues = ["{0:.2f}".format(np.max(maxs3, axis=0)[0]), 
             "{0:.2f}".format(-np.max(maxs3, axis=0)[1]), 
             str(-np.max(maxs3, axis=0)[2]), 
             "{0:.2f}".format(np.max(maxs3, axis=0)[3]), 
             "{0:.2f}".format(-np.max(maxs3, axis=0)[4]), 
             str(-np.max(cnstr[2]))]
#make a twin axis for toplabels
ax3t = ax3.twiny()
ax3t.set_yticks([])
ax3t.set_xticks([0,1,2,3,4])
ax3.set_xticklabels([minvalues[i]+'\n'+objs_labels[i] for i in range(len(objs_labels))])
ax3t.set_xticklabels(maxvalues)
plt.savefig('Objectives_parallel_axis_multiple_SOW.png')

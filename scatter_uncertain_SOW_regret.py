import os
import numpy as np
from matplotlib import pyplot
import pylab as p
from mpl_toolkits.mplot3d import Axes3D
pyplot.style.use('ggplot')

# Read in Latin hypercube samples of uncertain inputs
LHsamples = np.loadtxt('./parameter_samples.txt')
nSamples=len(LHsamples[:,0])
nObjs=4
nCnstr = 1
numPts = (len(os.listdir('./Generalized/resim_objs'))) # Get number of solutions on pareto front

def reformatData(method, nSamples):
    objs = np.zeros([numPts, nSamples, nObjs])
    if nCnstr>1:
        cnstr = np.zeros([numPts, nSamples, nCnstr])
    elif nCnstr==1:
        cnstr = np.zeros([numPts, nSamples])
    for i in range(numPts):
        objs[i,:,:] = np.loadtxt('./Generalized/resim_objs/' + method + '_objs_' + str(int(i)) + '.txt')
        if nCnstr>1:
            cnstr[i,:,:] = np.loadtxt('./Generalized/resim_cnstr/' + method + '_cnstr_' + str(int(i)) + '.txt')
        elif nCnstr==1:
            cnstr[i,:] = np.loadtxt('./Generalized/resim_cnstr/' + method + '_cnstr_' + str(int(i)) + '.txt')
        for j in range(nSamples):
            if objs[i,j,0]>0 or objs[i,j,3]>0:
                objs[i,j,:] = 0
    return objs, cnstr

a = 0.005
b = 0.5
c = 0.5
d = 0.1
h = 0.1
K = 2000
m = 0.7
sigmaX = 0.004
sigmaY = 0.004
SOW_inputs = [a, b, c, d, h, K, m, sigmaX, sigmaY]

# Calculate inequalities to use sort solutions into those that allow for coexistence
eq1 = LHsamples[:,3]*LHsamples[:,4]
eq1 = eq1[:, np.newaxis] # Need to turn this from an 1 dimensional array to a 2x1
eq2 = LHsamples[:,0]*np.power(LHsamples[:,4]*LHsamples[:,5],1-LHsamples[:,6])
eq2 = eq2[:, np.newaxis] # Need to turn this from an 1 dimensional array to a 2x1
eq3 = np.power(LHsamples[:,1],LHsamples[:,6])
eq3 = eq3[:, np.newaxis] # Need to turn this from an 1 dimensional array to a 2x1
# Append to samples array
LHsamples = np.concatenate((LHsamples, eq1, eq2, eq3), axis=1)

# Get lists of stable and unstable SOW
stable = [k for k in range(np.shape(LHsamples)[0]) if LHsamples[k,10] < LHsamples[k,11]]
unstable = [k for k in range(np.shape(LHsamples)[0]) if LHsamples[k,10] >= LHsamples[k,11]]

# Sort SOW into their average distance for the default SOW
average_diff = np.zeros(len(LHsamples[:,0]))
for j in range(len(LHsamples[:,0])):
    diff = 0
    for i in range(len(SOW_inputs)):
        diff += (LHsamples[j,i] - SOW_inputs[i])**2/np.var(LHsamples[:,i])
    average_diff[j] = np.sqrt(diff)
sorted_diff = np.argsort(average_diff)

# Stable SOW sorted by their distance to the default
stable_sorted = [SOW for SOW in sorted_diff if SOW in stable]

# Determine SOW distance from stability 
det_ext = [LHsamples[k,10] - LHsamples[k,11] for k in range(np.shape(LHsamples)[0])]
sorted_det = np.argsort(det_ext)
# Unstable SOW sorted by their distance to the inequality
unstable_sorted = [SOW for SOW in sorted_det if SOW in unstable]

reference = np.loadtxt('./Generalized.reference',delimiter=' ')
#reference_alternative1 = np.loadtxt('./Reoptimized_212.reference',delimiter=' ')
#reference_alternative2 = np.loadtxt('./Reoptimized_70.reference',delimiter=' ')
#reference_alternative3 = np.loadtxt('./Reoptimized_3489.reference',delimiter=' ')
reference[:,0] = -reference[:,0]
reference[:,3] = -reference[:,3]
#reference_alternative1[:,0] = -reference_alternative1[:,0]
#reference_alternative1[:,3] = -reference_alternative1[:,3]
#reference_alternative2[:,0] = -reference_alternative2[:,0]
#reference_alternative2[:,3] = -reference_alternative2[:,3]
#reference_alternative3[:,0] = -reference_alternative3[:,0]
#reference_alternative3[:,3] = -reference_alternative3[:,3]


# Get all objectives and constraints
objs, cnstr = reformatData('Previous_Prey', nSamples)

#ext_sol = [k for k in range(len(cnstr[:,212])) if cnstr[k,212]>0]
#def_sol = [k for k in range(len(objs[:,212,1])) if objs[k,212,1]>np.max(reference_alternative1[:,1])]
#reference_ext = reference[ext_sol,:]
#reference_def = reference[def_sol,:]
    
# Reformat objectives for right sign
objs[:,:,0] = -objs[:,:,0]
objs[:,:,3] = -objs[:,:,3]
#    
## Calculate metrics per solution on pareto front
#median = np.median(objs,axis=1)

fig = p.figure()
ax3D = Axes3D(fig)
cmap = pyplot.cm.get_cmap("tab20")
#Use obj6 for point size
#obj6_norm = (table.obj6-table.obj6.min())/(table.obj6.max()-table.obj6.min())
pts1 = ax3D.scatter(reference[:,0], reference[:,1], reference[:,3],
                    c=cmap(0.0),cmap=cmap, linewidth=0)
pts2 = ax3D.scatter(objs[:,stable_sorted[4],0], objs[:,stable_sorted[4],1], objs[:,stable_sorted[4],3],
                    c=cmap(0.15),cmap=cmap, linewidth=0)
#pts3 = ax3D.scatter(reference_alternative1[:,0], reference_alternative1[:,1], reference_alternative1[:,3],
#                    c=cmap(0.1),cmap=cmap, linewidth=0)
pts4 = ax3D.scatter(objs[:,stable_sorted[-1],0], objs[:,stable_sorted[-1],1], objs[:,stable_sorted[-1],3],
                    c=cmap(0.25),cmap=cmap, linewidth=0)
#pts5 = ax3D.scatter(reference_alternative2[:,0], reference_alternative2[:,1], reference_alternative2[:,3],
#                    c=cmap(0.2),cmap=cmap, linewidth=0)
pts6 = ax3D.scatter(objs[:,unstable_sorted[-1],0], objs[:,unstable_sorted[-1],1], objs[:,unstable_sorted[-1],3],
                    c=cmap(0.5),cmap=cmap, linewidth=0)
pts11 = ax3D.scatter(objs[:,unstable_sorted[0],0], objs[:,unstable_sorted[0],1], objs[:,unstable_sorted[0],3],
                    c=cmap(0.35),cmap=cmap, linewidth=0)
#pts12 = ax3D.scatter(reference_alternative3[:,0], reference_alternative3[:,1], reference_alternative3[:,3],
#                    c=cmap(0.3),cmap=cmap, linewidth=0)
pt_ideal = ax3D.scatter(12100, 0.0, 550, c='black', s=500, linewidth=0, marker='*')

ax3D.set_xlim(0,12000)
ax3D.set_xticks((np.arange(0,12005,4000)))
ax3D.set_ylim(0,1)
ax3D.set_yticks((np.arange(0,1.05,0.25)))
ax3D.set_zlim(0,510)
ax3D.set_zticks((np.arange(0,510,100)))
ax3D.set_facecolor('white')
# make the panes transparent
ax3D.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax3D.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax3D.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
# make the grid lines transparent
ax3D.xaxis._axinfo["grid"]['color'] =  'lightgray'
ax3D.yaxis._axinfo["grid"]['color'] =  'lightgray'
ax3D.zaxis._axinfo["grid"]['color'] =  'lightgray'
ax3D.set_xlabel("\nNet present value (NPV)")
ax3D.set_ylabel("\nPrey population deficit")
ax3D.set_zlabel("\nWorst harvest instance")

#fig.colorbar(cmap,ax=ax3D,shrink=0.75)
#fig.axes[-1].set_ylabel('Mean 1st percentile of consecutive low harvest')
#l0 = ax3D.scatter([],[],[], color='k', linewidth=0, depthshade=False)
#l1 = ax3D.scatter([],[],[], color='k', linewidth=0, depthshade=False)
#l2 = ax3D.scatter([],[],[], color='k', linewidth=0, depthshade=False)
#l3 = ax3D.scatter([],[],[], color='k', linewidth=0, depthshade=False)
#float_formatter = lambda x: "%.2f" % x
#np.set_printoptions(formatter={'float_kind':float_formatter})
#fig.legend([l0, l1, l2, l3],['a, b, c, d, h, K, m, sigmaX, sigmaY', str(SOW_inputs)[1:-1], str(LHsamples[sorted_diff[0]][0:9])[1:-1], str(LHsamples[sorted_diff[1]][0:9])[1:-1]], \
#    scatterpoints=1, title='SOW parameters', loc='lower right')
#legend = fig.legend([pts1,pts2,pts3,pts4,pts5,pts6],
#                    ['Solutions identified in assumed SOW',
#                     'Solutions reevaluated in nearby & stable SOW',
#                     'Solutions optimized to nearby & stable',
#                     'Solutions reevaluated in distant & stable SOW',
#                     'Solutions optimized to distant & stable SOW',
#                     'Solutions reevaluated in nearby & unstable SOW'])
#legend = fig.legend([pts1,pts2,pts3,pts4,pts5,pts6, pts11, pts12],
#                    [' ',
#                     ' ',
#                     ' ',
#                     ' ',
#                     ' ',
#                     ' ',
#                     ' ',
#                     ' '])
#frame = legend.get_frame()
#frame.set_facecolor('None')
#frame.set_edgecolor('None')
#ax3D.set_title("4 objective performance")

ax3D.view_init(10, -170)
    
p.show()
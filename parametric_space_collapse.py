import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.style.use('ggplot')
plt.ioff()

a = 0.005
b = 0.5
c = 0.5
d = 0.1
h = 0.1
K = 2000
m = 0.7
sigmaX = 0.004
sigmaY = 0.004
defaults = [a, b, c, d, h, K, m, sigmaX, sigmaY]

LHsamples = np.loadtxt('./parameter_samples.txt')
nSamples=len(LHsamples[:,0]) # Number of SOW
numPts = (len(os.listdir('./Generalized/resim_cnstr')))
no_harvest_collapse = np.loadtxt('./Zero_harvest_cnstr.txt')

cnstr = np.zeros([nSamples, numPts])
for i in range(numPts):
    cnstr[:,i] = np.loadtxt('./Generalized/resim_cnstr/Previous_Prey_cnstr_' + str(int(i)) + '.txt')

SatisfyMatrix = np.zeros([nSamples, numPts])
for i in range(np.shape(SatisfyMatrix)[0]):
    for j in range(np.shape(SatisfyMatrix)[1]):
        if cnstr[i,j] == 0:
            SatisfyMatrix[i,j] = 1 

reference = np.loadtxt('./Generalized.reference',delimiter=' ')
SOW_prob_all = np.mean(SatisfyMatrix, axis=1)
objs_labels = ["a", "b", "h", "K", "m"]

def inequality(b_val, m_val):
    return ((b_val**m_val)/(h*K)**(1-m_val))

# Calculate inequalities to use sort solutions into those that have an
# equilibrium and to those were the equilibrium is stable
eq1 = LHsamples[:,3]*LHsamples[:,4]
eq1 = eq1[:, np.newaxis] # Need to turn this from an 1 dimensional array to a 2x1
eq2 = LHsamples[:,0]*np.power(LHsamples[:,4]*LHsamples[:,5],1-LHsamples[:,6])
eq2 = eq2[:, np.newaxis] # Need to turn this from an 1 dimensional array to a 2x1
eq3 = np.power(LHsamples[:,1],LHsamples[:,6])
eq3 = eq3[:, np.newaxis] # Need to turn this from an 1 dimensional array to a 2x1
eq4 = inequality(LHsamples[:, 1],LHsamples[:,6])
eq4 = eq4[:, np.newaxis] # Need to turn this from an 1 dimensional array to a 2x1

# Append to samples array
LHsamples = np.concatenate((LHsamples, eq1, eq2, eq3, eq4), axis=1)

# Get lists of stable and unstable SOW
stable = [k for k in range(np.shape(LHsamples)[0]) if LHsamples[k,10] < LHsamples[k,11]]
unstable = [k for k in range(np.shape(LHsamples)[0]) if LHsamples[k,10] >= LHsamples[k,11]]
survival_possible = [k for k in range(np.shape(no_harvest_collapse)[0]) if no_harvest_collapse[k] == 0]
survival_impossible = [k for k in range(np.shape(no_harvest_collapse)[0]) if no_harvest_collapse[k] > 0]

# Sort SOW into their average distance for the default SOW
average_diff = np.zeros(len(LHsamples[:,0]))
diff = np.zeros(len(defaults))
for j in range(len(LHsamples[:,0])):
    for i in range(len(defaults)):
        diff[i] = np.absolute(defaults[i]-LHsamples[j,i])/defaults[i]
    average_diff[j] = np.mean(diff)
sorted_diff = np.argsort(average_diff)

# Stable and unstable SOW sorted by their distance to the default
stable_sorted = [SOW for SOW in sorted_diff if SOW in stable]
unstable_sorted = [SOW for SOW in sorted_diff if SOW in unstable]

ineq_parameters = LHsamples[:,[0,1,4,5,6]]

cmap = plt.cm.get_cmap("RdBu")
cmap2 = plt.cm.get_cmap("tab20")

X = np.arange(0.005,1,0.001)
Y = np.arange(0.1,1.5,0.001)
X, Y = np.meshgrid(X, Y)
Z = inequality(X, Y)
Z = Z.clip(0,2)

fig = plt.figure(figsize=(12,9))
ax3D = fig.gca(projection='3d')
pts_ineq = ax3D.plot_surface(X, Y, Z, color='black', alpha=0.25)
pts1 = ax3D.scatter(ineq_parameters[survival_possible, 1], ineq_parameters[survival_possible, 4], ineq_parameters[survival_possible, 0], 
                    c=SOW_prob_all[survival_possible],cmap=cmap, s=20, alpha=0.7)
pts2 = ax3D.scatter(ineq_parameters[survival_impossible, 1], ineq_parameters[survival_impossible, 4], ineq_parameters[survival_impossible, 0], 
                    c=SOW_prob_all[survival_impossible], cmap=cmap, s=4, alpha=0.7)
pts3 = ax3D.scatter(ineq_parameters[1540, 1], ineq_parameters[1540, 4], ineq_parameters[1540, 0], color='none', edgecolor=cmap2(0.1), linewidth='2',cmap=cmap, s=100)
pts4 = ax3D.scatter(ineq_parameters[2832, 1], ineq_parameters[2832, 4], ineq_parameters[2832, 0], color='none', edgecolor=cmap2(0.2), linewidth='2',cmap=cmap, s=100)
pts5 = ax3D.scatter(ineq_parameters[1253, 1], ineq_parameters[1253, 4], ineq_parameters[1253, 0], color='none', edgecolor=cmap2(0.3), linewidth='2',cmap=cmap, s=100)
pts6 = ax3D.scatter(ineq_parameters[2951, 1], ineq_parameters[2951, 4], ineq_parameters[2951, 0], color='none', edgecolor=cmap2(0.5), linewidth='2',cmap=cmap, s=100)
pt_ref = ax3D.scatter(defaults[1], defaults[6], defaults[0], c=cmap2(0.0),cmap=cmap, s=100)
sm = plt.cm.ScalarMappable(cmap=cmap)
sm.set_array([SOW_prob_all.min()*100,SOW_prob_all.max()*100])
fig.colorbar(sm,ax=ax3D,shrink=0.75)
fig.axes[-1].set_ylabel('Percentage of solutions without predator collapse')
ax3D.set_xlabel("b")
ax3D.set_ylabel("m")
ax3D.set_zlabel("a")
ax3D.set_zlim([0.0,2.0])
ax3D.set_xlim([0.0,1.0])
ax3D.set_ylim([0.0,1.5])
ax3D.xaxis.set_view_interval(0,  0.5)
ax3D.set_facecolor('white')
ax3D.view_init(12, -17)
#fig.legend([pts1,pts2,pts3,pts4,pts5,pts6,pt_ref],[' ',' ',' ',' ',' ',' ',' '])
plt.savefig('parametric_space_collapse.png')


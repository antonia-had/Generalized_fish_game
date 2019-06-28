import os
import numpy as np

nSamples=4000
nObjs=5
nCnstr = 1
LHsamples = np.loadtxt('./parameter_samples.txt')
no_harvest_collapse = np.loadtxt('./Zero_harvest_cnstr.txt')
# Calculate inequalities to use sort solutions into those that have an
# equilibrium and to those were the equilibrium is stable
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
survival_possible = [k for k in range(np.shape(no_harvest_collapse)[0]) if no_harvest_collapse[k] == 0]

def reformatData(method, nSamples):
    numPts = (len(os.listdir('./Generalized/resim_objs')))
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
    return objs, cnstr

def calcSatisfaction(objs,cnstr):
    '''Calculates the percent of SOWs in which the satisficing criteria are met.'''
    SatisfyMatrix = np.zeros([np.shape(objs)[0],np.shape(objs)[1], nObjs+nCnstr+1])
    for i in range(np.shape(SatisfyMatrix)[0]):
        for j in range(np.shape(SatisfyMatrix)[1]):
            if objs[i,j,0] <= -1500:
                SatisfyMatrix[i,j,0] = 1
            if objs[i,j,1] <= 0.5:
                SatisfyMatrix[i,j,1] = 1
            if objs[i,j,2] <= 5:
                SatisfyMatrix[i,j,2] = 1
            if objs[i,j,3] <= -50:
                SatisfyMatrix[i,j,3] = 1
            if objs[i,j,4] <= 2300:
                SatisfyMatrix[i,j,4] = 1
            if cnstr[i,j] <= 0:
                SatisfyMatrix[i,j,5] = 1                 
            if objs[i,j,0] <= -1500 and objs[i,j,1] <= 0.5 and objs[i,j,2] <= 5 and objs[i,j,3] <= -50 and objs[i,j,4] <= 2300 and cnstr[i,j] <= 0:
                SatisfyMatrix[i,j,6] = 1
                
    satisfaction = np.zeros([np.shape(SatisfyMatrix)[0],np.shape(SatisfyMatrix)[2]])
    for i in range(np.shape(SatisfyMatrix)[0]):
        for j in range(np.shape(SatisfyMatrix)[2]):
            satisfaction[i,j] = np.mean(SatisfyMatrix[i,:,j])
    
    return satisfaction

strategies = ['Previous_Prey']
for i in range(len(strategies)):
    objs, cnstr = reformatData(strategies[i], nSamples)
    satisfaction = calcSatisfaction(objs[:,survival_possible,:],cnstr[:,survival_possible])
    np.savetxt('Robustness.txt', satisfaction, delimiter=' ')
 

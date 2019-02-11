import numpy as np
from generalized_fish_game import fish_game

# Read in Latin hypercube samples of uncertain parameters
LHsamples = np.loadtxt('./parameter_samples.txt')

# Read in result files from optimization
Previous_Prey = np.loadtxt('./Zero_harvest.resultfile')

# Define the number of objectives and constraints
nObjs = 4 
nCnstr = 1 

# Initialize matrices to store all objectives and constraints when evaluating these policies
# across all Latin hypercube samples of uncertain parameter values
Previous_Prey_objs = np.zeros([np.shape(LHsamples)[0],nObjs])
Previous_Prey_cnstr = np.zeros([np.shape(LHsamples)[0],nCnstr])

# Run simulation
for j in range(np.shape(LHsamples)[0]):
    additional_inputs = np.append(['Previous_Prey'], 
                                  [LHsamples[j,0], 
                                   LHsamples[j,1], 
                                   LHsamples[j,2], 
                                   LHsamples[j,3], 
                                   LHsamples[j,4], 
                                   LHsamples[j,5], 
                                   LHsamples[j,6], 
                                   LHsamples[j,7], 
                                   LHsamples[j,8]])
    Previous_Prey_objs[j,:],Previous_Prey_cnstr[j,:] = fish_game(Previous_Prey[0:6], additional_inputs)
# Write output to file labeled by Pareto point index
filename_obj = "./Zero_harvest/resim_objs/Zero_harvest_objs.txt"
np.savetxt(filename_obj, Previous_Prey_objs[:,:])
filename_cnstr = "./Zero_harvest/resim_cnstr/Zero_harvest_cnstr.txt"
np.savetxt(filename_cnstr, Previous_Prey_cnstr[:,:])

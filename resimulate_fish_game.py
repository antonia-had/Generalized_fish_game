import math
import numpy as np
from mpi4py import MPI
from generalized_fish_game import fish_game

# Read in Latin hypercube samples of uncertain parameters
LHsamples = np.loadtxt('./parameter_samples.txt')

# Read in result files from optimization
Previous_Prey = np.loadtxt('./Generalized.resultfile')

# Define the number of objectives and constraints
nObjs = 5 
nCnstr = 1 

# Begin parallel simulation
comm = MPI.COMM_WORLD

# Get the number of processors and the rank of processors
rank = comm.rank
nprocs = comm.size

# Determine the chunk which each processor will neeed to do
count = int(math.floor(np.shape(Previous_Prey)[0]/nprocs))
remainder = np.shape(Previous_Prey)[0] % nprocs

# Use the processor rank to determine the chunk of work each processor will do
if rank < remainder:
	start = rank*(count+1)
	stop = start + count + 1
else:
	start = remainder*(count+1) + (rank-remainder)*count
	stop = start + count

# Initialize matrices to store all objectives and constraints when evaluating these policies
# across all Latin hypercube samples of uncertain parameter values
Previous_Prey_objs = np.zeros([stop-start,np.shape(LHsamples)[0],nObjs])
Previous_Prey_cnstr = np.zeros([stop-start,np.shape(LHsamples)[0],nCnstr])

# Run simulation
for i in range(start, stop):
    row = i-start
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
        Previous_Prey_objs[row,j,:],Previous_Prey_cnstr[row,j,:] = fish_game(Previous_Prey[i,0:6], additional_inputs)
    # Write output to file labeled by Pareto point index
    filename_obj = "./Generalized/resim_objs/Previous_Prey_objs_%i.txt" % i
    np.savetxt(filename_obj, Previous_Prey_objs[row,:,:])
    filename_cnstr = "./Generalized/resim_cnstr/Previous_Prey_cnstr_%i.txt" % i
    np.savetxt(filename_cnstr, Previous_Prey_cnstr[row,:,:])

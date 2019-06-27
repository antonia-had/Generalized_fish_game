import numpy as np
from math import *
import os
from generalized_fish_game import fish_game

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

def optimize_fish_game():
    # For some reason this needs to be imported inside the function
    import borg as bg

    strategies = ['Previous_Prey']

    parallel = 1 # 1= master-slave (parallel), 0=serial

    nRBF = 2 # no. of RBFs to use
    nIn = 1 # no. of inputs (depending on selected strategy)
    nVars = nIn*nRBF*3 # no. of variables to be optimized. ( no. of inputs * no. of RBFs * [center, radius, weight])
    nObjs = 5 # no. of objectives to optimize for
    nCnstr = 1 # no. of constraints
    
    # Set optimization settings
    nSeeds = 20
    dVar_range = [0, 1] # define decision variable (C, R, W) range
    epsilons = [0.0001]*nObjs # set epsilon values for objectives
    NFEs = 3000 # number of function evaluations for Borg to perform
    runtime_freq = 500  # Interval at which to print runtime details for each random seed

    # If using master-slave, start MPI. Only do once.
    if parallel == 1:
        bg.Configuration.startMPI()  # start parallelization with MPI

    for selected_strategy in strategies:
        for j in range(nSeeds):

            # Create array containing the strategy to run & the SOW parameters
            additional_inputs = np.append([selected_strategy],[SOW_inputs])

            # Instantiate borg class
            borg = bg.Borg(nVars, # number of variables
                           nObjs, # number of objectives
                           nCnstr, # number of constraints
                           fish_game, # function to optimize
                           additional_inputs = additional_inputs)

            # Set bounds and epsilon values
            borg.setBounds(*[dVar_range]*nVars)
            borg.setEpsilons(*epsilons)

            # Define runtime file path for each seed:
            runtime_filename = os.getcwd() + '/Generalized/runtime/' + selected_strategy + '_' + str(j+1) + '.runtime'

            if parallel == 1:
                # Run parallel Borg
                result = borg.solveMPI(maxEvaluations=NFEs, runtime=runtime_filename)

            if parallel == 0:
                # Run serial Borg
                result = borg.solve({"maxEvaluations": NFEs,
                                     "runtimeformat": 'borg',
                                     "frequency": runtime_freq,
                                     "runtimefile": runtime_filename})

            if result:
                # This particular seed is now finished being run in parallel. The result will only be returned from
                # one node in case running Master-Slave Borg.
                result.display()

                # Create/write objective values and decision variable values to files in folder "sets", 1 file per seed.
                f1 = open(os.getcwd() + '/Generalized/sets/' + selected_strategy + '_' + str(j+1) + '.set', 'w')
                for solution in result:
                    line = ''
                    for i in range(len(solution.getVariables())):
                        line = line + (str(solution.getVariables()[i])) + ' '

                    for i in range(len(solution.getObjectives())):
                        line = line + (str(solution.getObjectives()[i])) + ' '
                    f1.write(line[0:-1] + '\n')
                f1.write("#")
                f1.close()

                # Create/write only objective values to files in folder "objs", 1 file per seed. Purpose is so that
                # the file can be processed in MOEAFramework, where performance metrics may be evaluated across seeds.
                f2 = open(os.getcwd() + '/Generalized/objs/' + selected_strategy + '_' + str(j+1) + '.obj', 'w')
                for solution in result:
                    line = ''
                    for i in range(len(solution.getObjectives())):
                        line = line + (str(solution.getObjectives()[i])) + ' '

                    f2.write(line[0:-1]+'\n')
                f2.write("#")
                f2.close()

                # Create/write only objective values to files in folder "objs", 1 file per seed. Purpose is so that
                # the file can be processed in MOEAFramework, where performance metrics may be evaluated across seeds.
                f3 = open(os.getcwd() + '/Generalized/cnstrs/' + selected_strategy + '_' + str(j+1) + '.cnstr', 'w')
                for solution in result:
                    line = ''
                    for i in range(len(solution.getConstraints())):
                        line = line + (str(solution.getConstraints()[i])) + ' '

                    f3.write(line[0:-1]+'\n')
                f3.write("#")
                f3.close()

                print("Seed %s complete") %j

    if parallel == 1:
        bg.Configuration.stopMPI()  # stop parallel function evaluation process

    return None

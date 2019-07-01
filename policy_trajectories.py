import numpy as np
import itertools
import matplotlib.pyplot as plt
from cycler import cycler
plt.style.use('ggplot')

nRBF = 2 # no. of RBFs to use
nIn = 1 # no. of inputs (depending on selected strategy)
nOut = 1 # no. of outputs (depending on selected strategy)
nVars = nIn*nRBF*3 # no. of variables to be optimized. ([Center, radius, weight] * no. of RBFs * no. of inputs)

# Default SOW parameters
a = 0.005
b = 0.5
c = 0.5
d = 0.1
h = 0.1
K = 2000
m = 0.7
sigmaX = 0.004
sigmaY = 0.004

defaultSOW = [a, b, c, d, h, K, m, sigmaX, sigmaY]
tSteps = 100 # no. of timesteps to run the fish game on
strategy = 'Previous_Prey'
results = np.loadtxt("./Generalized.resultfile")
robustness = np.loadtxt('./Robustness.txt',delimiter=' ')
LHsamples = np.loadtxt('./parameter_samples.txt')
# Pick solutions of interest 
NPV_robust = np.argmax(robustness[:,0])
all_robust = np.argmax(robustness[:,-1])

# Define problem to be solved
def fish_game(vars, # contains all C, R, W
              additional_inputs # Contains defined management strategy and SOW params
              ):

    # Get system behavior parameters (need to convert from string to float)
    a = float(additional_inputs[2])
    b = float(additional_inputs[3])
    c = float(additional_inputs[4])
    d = float(additional_inputs[5])
    h = float(additional_inputs[6])
    K = float(additional_inputs[7])
    m = float(additional_inputs[8])
    sigmaX = float(additional_inputs[9])
    sigmaY = float(additional_inputs[10])

    x = np.zeros(tSteps+1) # Create prey population array
    y = np.zeros(tSteps+1) # Create predator population array
    z = np.zeros(tSteps+1) # Create harvest array
    harvest = np.zeros(tSteps+1)
    NPVharvest = np.zeros(tSteps+1)
    # Create array with environmental stochasticity for prey
    epsilon_prey = np.random.normal(0.0, sigmaX, 1)
    
    # Create array with environmental stochasticity for predator
    epsilon_predator = np.random.normal(0.0, sigmaY, 1)

    # Initialize populations and values
    x[0] = additional_inputs[0]
    y[0] = additional_inputs[1]
    z[0] = hrvSTR([x[0]], vars, [[0, K]], [[0, 1]])
    NPVharvest[0] = harvest[0] = z[0]*x[0]
    if additional_inputs[0]>K:
        input_ranges = [[0, additional_inputs[0]]] # Prey pop. range to use for normalization
    else:
        input_ranges = [[0, K]] # Prey pop. range to use for normalization
    output_ranges = [[0, 1]] # Range to de-normalize harvest to    
    # Go through all timesteps for prey, predator, and harvest
    for t in range(tSteps):
        if x[t] > 0 and y[t] > 0:
            x[t+1] = (x[t] + b*x[t]*(1-x[t]/K) - (a*x[t]*y[t])/(np.power(y[t],m)+a*h*x[t]) - z[t]*x[t])* np.exp(epsilon_prey) # Prey growth equation
            y[t+1] = (y[t] + c*a*x[t]*y[t]/(np.power(y[t],m)+a*h*x[t]) - d*y[t]) *np.exp(epsilon_predator) # Predator growth equation
            if t <= tSteps-1:
                z[t+1] = hrvSTR([x[t]], vars, input_ranges, output_ranges)
                harvest[t+1] = z[t+1]*x[t+1]
                NPVharvest[t+1] = NPVharvest[t] + harvest[t+1]*(1+0.05)**(-(t+1))
        else:
            NPVharvest[t+1] = NPVharvest[t]
    low_hrv = [harvest[j]<x[j]/20 for j in range(len(harvest))]
    count = [ sum( 1 for _ in group ) for key, group in itertools.groupby( low_hrv ) if key ]
    if count: # Checks if theres at least one count (if not, np.max won't work on empty list)
        cons_low_harv = np.max(count)  # Finds the largest number of consecutive low harvests
    else:
        cons_low_harv = 0
    harv_1st_pc = np.percentile(harvest,1)
    variance = np.var(harvest)
                    
    return [x, y, z, NPVharvest], [NPVharvest[100], np.mean((K-x)/K), cons_low_harv, harv_1st_pc, variance, (y < 1).sum()]

# Calculate outputs (u) corresponding to each sample of inputs
# u is a 2-D matrix with nOut columns (1 for each output)
# and as many rows as there are samples of inputs
def hrvSTR(Inputs, vars, input_ranges, output_ranges):
    # Rearrange decision variables into C, R, and W arrays
    # C and R are nIn x nRBF and W is nOut x nRBF
    # Decision variables are arranged in 'vars' as nRBF consecutive
    # sets of {nIn pairs of {C, R} followed by nOut Ws}
    # E.g. for nRBF = 2, nIn = 3 and nOut = 4:
    # C, R, C, R, C, R, W, W, W, W, C, R, C, R, C, R, W, W, W, W
    C = np.zeros([nIn,nRBF])
    R = np.zeros([nIn,nRBF])
    W = np.zeros([nOut,nRBF])
    for n in range(nRBF):
        for m in range(nIn):
            C[m,n] = vars[(2*nIn+nOut)*n + 2*m]
            R[m,n] = vars[(2*nIn+nOut)*n + 2*m + 1]
        for k in range(nOut):
            W[k,n] = vars[(2*nIn+nOut)*n + 2*nIn + k]

    # Normalize weights to sum to 1 across the RBFs (each row of W should sum to 1)
    totals = np.sum(W,1)
    for k in range(nOut):
        if totals[k] > 0:
            W[k,:] = W[k,:]/totals[k]
    # Normalize inputs
    norm_in = np.zeros(nIn)
    for m in range (nIn):
        norm_in[m] = (Inputs[m]-input_ranges[m][0])/(input_ranges[m][1]-input_ranges[m][0])
    # Create array to store outputs
    u = np.zeros(nOut)
    # Calculate RBFs
    for k in range(nOut):
        for n in range(nRBF):
            BF = 0
            for m in range(nIn):
                if R[m,n] > 10**-6: # set so as to avoid division by 0
                    BF = BF + ((norm_in[m]-C[m,n])/R[m,n])**2
                else:
                    BF = BF + ((norm_in[m]-C[m,n])/(10**-6))**2
            u[k] = u[k] + W[k,n]*np.exp(-BF)
    # De-normalize outputs
    norm_u = np.zeros(nOut)
    for k in range(nOut):
        norm_u[k] = output_ranges[k][0] + u[k]*(output_ranges[k][1]-output_ranges[k][0])
    return norm_u

cmap = plt.cm.get_cmap("plasma")
highprofitpolicy = results[NPV_robust,0:6]
mostrobustpolicy = results[all_robust,0:6]
ntraj = 5 # Number of trajectories to plot
worlds = [defaultSOW, LHsamples[1540,0:9].tolist(), LHsamples[85,0:9].tolist()]

# Different SOW have different possible trajectories
x = np.zeros([len(worlds), ntraj])
y = np.zeros([len(worlds), ntraj])
# When unharvested, different SOWs have different "natural populations" which need to be determined
eq_x = [1900, 1165, 720]
eq_y = [240, 1300, 500]
for i in range(len(worlds)):
    x[i] = np.linspace(eq_x[i]*0.95, eq_x[i]*1.05, ntraj)
    y[i] = np.linspace(eq_y[i]*0.95, eq_y[i]*1.05, ntraj)
nCrit = 5 + 1 # 5 Objectives + 1 Constraint

noharv = np.zeros([len(worlds), ntraj, 4, tSteps+1])
highprofitharv = np.zeros([len(worlds), ntraj, 4, tSteps+1]) # SOW, initial conditions, fish pop., timesteps
robustharv = np.zeros([len(worlds), ntraj, 4, tSteps+1]) # SOW, initial conditions, fish pop., timesteps
highprofitOBJ = np.zeros([len(worlds), ntraj, nCrit]) # SOW, initial conditions, criteria
robustOBJ = np.zeros([len(worlds), ntraj, nCrit]) # SOW, initial conditions, criteria
noharvOBJ = np.zeros([len(worlds), ntraj, nCrit]) 

for j in range(len(highprofitharv[:,:,:])): # Loop through SOW
    for i in range(len(highprofitharv[0,:,:])): # Loop through initial conditions
        additional_inputs = np.append([x[j,i],y[j,i]], worlds[j])
        highprofitharv[j,i,:], highprofitOBJ[j,i] = fish_game(highprofitpolicy, additional_inputs)
        highprofitharv[j,i][0:2] = highprofitharv[j,i][0:2].clip(0,5000)
        robustharv[j,i,:], robustOBJ[j,i] = fish_game(mostrobustpolicy,additional_inputs)
        robustharv[j,i][0:2] = robustharv[j,i][0:2].clip(0,5000)
        noharv[j,i,:], noharvOBJ[j,i] = fish_game([0.0]*6,additional_inputs)

nb_points   = 100
y_iso = [np.linspace(0, 300, nb_points), np.linspace(0, 1500, nb_points), np.linspace(0, 600, nb_points)]

def isoclines(y, SOW):
    a = float(SOW[0])
    b = float(SOW[1])
    c = float(SOW[2])
    d = float(SOW[3])
    h = float(SOW[4])
    K = float(SOW[5])
    m = float(SOW[6])
    return ([(y**m*d)/(a*(c-h*d)),
             K*b/(2*b)-y**m/(2*a*h)+K*np.sqrt((a*h*b+y**m*b/K)**2-4*a**2*h*b*y/K)/(2*a*h*b)])
    
iso1= np.zeros([len(worlds), nb_points]) # y isocline
iso2= np.zeros([len(worlds), nb_points]) # x isocline

for j in range(len(worlds)):
    iso1[j], iso2[j] = isoclines(y_iso[j], worlds[j])

ncols = 3

fig =  plt.figure(figsize=(18,9))
for l in range(ncols):
    ax = fig.add_subplot(1,ncols,l+1)
    ax.plot(iso1[l],y_iso[l], c='gray')
    ax.plot(iso2[l],y_iso[l], c='gray')
    for n in range(len(highprofitharv[0,:,:])): # Loop through initial conditions
        ax.set_prop_cycle(cycler('color', [cmap(1.*highprofitharv[l,n,2][i]) for i in range(tSteps)]))
        for i in range(tSteps):
            line1 = ax.plot(highprofitharv[l,n,0][i:i+2], highprofitharv[l,n,1][i:i+2], linewidth=2, linestyle='--',label='Most robust in NPV')
        ax.set_prop_cycle(cycler('color', [cmap(1.*robustharv[l,n,2][i]) for i in range(tSteps)]))
        for i in range(tSteps):
            line2 = ax.plot(robustharv[l,n,0][i:i+2], robustharv[l,n,1][i:i+2], linewidth=2, linestyle='-',label='Most robust in all criteria')
#            ax.set_prop_cycle(cycler('color', [cmap(1.*noharv[ncols*k+l,n,2][i]) for i in range(tSteps)]))
#            for i in range(tSteps):
#                line3 = ax.plot(noharv[ncols*k+l,n,0][i:i+2], noharv[ncols*k+l,n,1][i:i+2], linewidth=2, linestyle='-',label='No harvest')
        endpoint1 = ax.scatter(highprofitharv[l,n,0][100], highprofitharv[l,n,1][100], c='darkgoldenrod', s=20)
        endpoint2 = ax.scatter(robustharv[l,n,0][100], robustharv[l,n,1][100], c='gold', s=20)
#            endpoint3 = ax.scatter(noharv[ncols*k+l,n,0][100], noharv[ncols*k+l,n,1][100], c='black', s=20)
        collapse_thres = ax.axvline(x=worlds[l][5]*0.5*0.2, linestyle=':', c='crimson')
        overfishing_thres = ax.axvline(x=worlds[l][5]*0.5*0.5, linestyle=':', c='purple')
    ax.set_xlabel("Prey")
#        ax.set_ylim(0,305)
#        ax.set_xlim(0,2500)
    if l==0:
        ax.set_ylabel("Predator")        
#        if l==2:       
#            ax.legend([endpoint1, endpoint2, pop_thres],['Most robust in NPV equilibrium point','Most robust in all criteria equilibrium point','Population threshold'], loc = 'lower right')
sm = plt.cm.ScalarMappable(cmap=cmap)
sm.set_array([0.0,1.0])
fig.subplots_adjust(bottom = 0.2)
cbar_ax = fig.add_axes([0.1, 0.06, 0.8, 0.06])
cb = fig.colorbar(sm, cax=cbar_ax, orientation="horizontal")
cb.ax.set_xlabel("Ratio of prey harvested")
plt.show()
plt.savefig("policy_trajectories.png")
plt.savefig("policy_trajectories.svg")



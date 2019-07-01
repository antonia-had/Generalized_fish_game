import numpy as np
import itertools
import matplotlib.pyplot as plt
plt.style.use('ggplot')

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
LHsamples = np.loadtxt('./parameter_samples.txt')

def fish_game(additional_inputs # Contains defined management strategy and SOW params
              ):

    # Get system behavior parameters (need to convert from string to float)
    a = float(additional_inputs[0])
    b = float(additional_inputs[1])
    c = float(additional_inputs[2])
    d = float(additional_inputs[3])
    h = float(additional_inputs[4])
    K = float(additional_inputs[5])
    m = float(additional_inputs[6])
    sigmaX = float(additional_inputs[7])
    sigmaY = float(additional_inputs[8])

    x = np.zeros(tSteps+1) # Create prey population array
    y = np.zeros(tSteps+1) # Create predator population array

    # Create array with environmental stochasticity for prey
    epsilon_prey = np.random.normal(0.0, sigmaX, 1)
    
    # Create array with environmental stochasticity for predator
    epsilon_predator = np.random.normal(0.0, sigmaY, 1)

    # Initialize populations and values
    x[0] = K
    y[0] = 250   
    # Go through all timesteps for prey and predator (no harvest)
    for t in range(tSteps):
        if x[t] > 0 and y[t] > 0:
            x[t+1] = (x[t] + b*x[t]*(1-x[t]/K) - (a*x[t]*y[t])/(np.power(y[t],m)+a*h*x[t]) - 0*x[t])* np.exp(epsilon_prey) # Prey growth equation
            y[t+1] = (y[t] + c*a*x[t]*y[t]/(np.power(y[t],m)+a*h*x[t]) - d*y[t]) *np.exp(epsilon_predator) # Predator growth equation
    x = x.clip(0) 
    y = y.clip(0)               
    return [x, y]

cmap = plt.cm.get_cmap("coolwarm_r")


fig =  plt.figure(figsize=(18,9))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)
for i in range((len(LHsamples[:,0]))):
    x, y = fish_game(LHsamples[i,0:9])
    norm_color = (LHsamples[i,5]-LHsamples[:,5].min())/(LHsamples[:,5].max()-LHsamples[:,5].min())     
    ax1.plot(np.arange(tSteps+1), x, c = cmap(norm_color), alpha = 0.5)
    ax2.plot(np.arange(tSteps+1), y, c = cmap(norm_color), alpha = 0.5)

ax1.set_xlabel('Time')
ax2.set_xlabel('Time')
ax1.set_ylabel('Prey population')
ax2.set_ylabel('Predator population')

sm = plt.cm.ScalarMappable(cmap=cmap)
sm.set_array([LHsamples[:,5].min(),LHsamples[:,5].max()])
cbar = fig.colorbar(sm)
cbar.ax.set_ylabel("\nSampled carrying capacity (K)")

plt.savefig('sampledKvspopulations.png')
plt.savefig('sampledKvspopulations.svg')

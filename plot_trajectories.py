'''This script was written by Antonia Hadjimichael, adapting the script found here: https://scipy-cookbook.readthedocs.io/items/LoktaVolterraTutorial.html
'''
import numpy as np
import pylab as p
from matplotlib import pyplot as plt
from scipy import integrate
plt.style.use('ggplot')
plt.switch_backend('agg')
plt.ioff()


LHsamples = np.loadtxt('./parameter_samples.txt')

# Default SOW parameters
a = 0.005
b = 0.5
c = 0.5
d = 0.1
h = 0.1
K = 2000
m = 0.7

sample = 1253

a = LHsamples[sample,0]
b = LHsamples[sample,1]
c = LHsamples[sample,2]
d = LHsamples[sample,3]
h = LHsamples[sample,4]
K = LHsamples[sample,5]
m = LHsamples[sample,6]

np.seterr(divide='ignore', invalid='ignore') # This is to ignore RuntimeWarning: invalid value encountered in true_divide (When both populations die)

if m>0:
    def fish(P, t=0):
        return ([b*P[0]*(1-P[0]/K)                         - (a*P[0]*P[1])/(P[1]**m+a*h*P[0]), #P[0] is prey, P[1] is predator
                 c*a*P[0]*P[1]/(P[1]**m+a*h*P[0]) - d*P[1]                                   ])

    EQ_1 = ([K,0])
    EQ_2 = ([K*(1-(a*(c-d*h))/(b*c)),(K*(1-(a*(c-d*h))/(b*c)))*(a*(c-d*h))/d]) # This is actually the nontrivial equilibrium for m=1 (for simplification)
    all(fish(EQ_1) == np.zeros(2) ) and all(fish(EQ_2) == np.zeros(2)) # Checking if the calculated equilibria are correct
    
    ## Integration
    t = np.linspace(0, 150,  1000)              # time
    P0 = np.array([1000, 1000])                     # initial conditions
    P, infodict = integrate.odeint(fish, P0, t, full_output=True)
    infodict['message']                     # >>> 'Integration successful.'
#    
    # Plot population numbers
    prey, predator = P.T
    f1 = p.figure()
    p.plot(t, prey, 'r-', label='Prey')
    p.plot(t, predator  , 'b-', label='Predator')
    p.grid()
    p.legend(loc='best')
    p.xlabel('time')
    p.ylabel('population')
    p.title('Evolution of predator and prey populations')
    
    # Plotting direction fields and trajectories
    values  = np.linspace(1,5, 10)            # position of P0 between EQ_1 and EQ_2
    vcolors = p.cm.autumn_r(np.linspace(0.1, 1, len(values)))  # colors for each trajectory
    f2 = p.figure()
    
    # plot trajectories
    for v, col in zip(values, vcolors):
        P0 = [E*v for E in [800,500]]             # starting point for each directory                            
        P = integrate.odeint(fish, P0, t)         # we don't need infodict here
        p.plot( P[:,0], P[:,1], lw=1.5, color=col, label='P0=(%.f, %.f)' % ( P0[0], P0[1]) )
    
    # define a grid and compute direction at each point
    ymax = p.ylim(ymin=0)[1]                        # get axis limits
    xmax = p.xlim(xmin=0)[1]
    nb_points   = 20
    
    x = np.linspace(0, xmax, nb_points)
    y = np.linspace(0, ymax, nb_points)
    
    X1 , Y1  = np.meshgrid(x,y)                    # create a grid
    DX1, DY1 = fish([X1, Y1])                      # compute growth rate on the grid
    M = (np.hypot(DX1, DY1))                       # Norm of the growth rate 
    M[ M == 0] = 1.                                # Avoid zero division errors 
    DX1 /= M                                       # Normalize each arrow
    DY1 /= M
    
    def isoclines(y):
        return ([(y**m*d)/(a*(c-h*d)),
                 K*b/(2*b)-y**m/(2*a*h)+K*np.sqrt((a*h*b+y**m*b/K)**2-4*a**2*h*b*y/K)/(2*a*h*b)])
    iso1, iso2 = isoclines(y)
    
    # Draw direction fields, using matplotlib 's quiver function
    # I choose to plot normalized arrows and to use colors to give information on
    # the growth speed
    p.title('Trajectories and direction fields')
    Q = p.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=p.cm.plasma)
    p.plot(iso1,y, c='black')
    p.plot(iso2,y, c='black')
    p.xlabel('Prey abundance')
    p.ylabel('Predator abundance')
    #p.legend()
    p.grid()
    p.xlim(0, xmax)
    p.ylim(0, ymax)
    p.show()

if m==0:
    def fish(P, t=0):
        return ([b*P[0]*(1-P[0]/K)            - (a*P[0]*P[1])/(1+a*h*P[0]), #P[0] is prey, P[1] is predator
                 c*(a*P[0]*P[1])/(1+a*h*P[0]) - d*P[1]                   ])

    EQ_1 = ([K,0])
    EQ_2 = ([d/(a*(c-d*h)),b*(1+a*h*(d/(a*(c-d*h))))*(1-(d/(a*(c-d*h)))/K)/a])
#    all(fish(EQ_1) == np.zeros(2) ) and all(fish(EQ_2) == np.zeros(2)) # Checking if the calculated equilibria are correct
    
    # Integration
    t = np.linspace(0, 150,  1000)              # time
    P0 = np.array([100, 80])                     # initial conditions
    P, infodict = integrate.odeint(fish, P0, t, full_output=True)
    infodict['message']                     # >>> 'Integration successful.'
    
    # Plot population numbers
    prey, predator = P.T
    f1 = p.figure()
    p.plot(t, prey, 'r-', label='Prey')
    p.plot(t, predator  , 'b-', label='Predator')
    p.grid()
    p.legend(loc='best')
    p.xlabel('time')
    p.ylabel('population')
    p.title('Evolution of predator and prey populations')
    
    # Plotting direction fields and trajectories
    values  = np.linspace(0.1, 4, 10)            # position of P0 between EQ_1 and EQ_2
    vcolors = p.cm.autumn_r(np.linspace(0.1, 1, len(values)))  # colors for each trajectory
    f2 = p.figure()
    
    # plot trajectories
    for v, col in zip(values, vcolors):
        P0 = [E*v for E in EQ_2]                  # starting point                             
        P = integrate.odeint(fish, P0, t)         # we don't need infodict here
        p.plot( P[:,0], P[:,1], lw=0.5*v, color=col, label='P0=(%.f, %.f)' % ( P0[0], P0[1]) )
    
    # define a grid and compute direction at each point
    ymax = p.ylim(ymin=0)[1]                        # get axis limits
    xmax = p.xlim(xmin=0)[1]
    nb_points   = 20
    
    x = np.linspace(0, xmax, nb_points)
    y = np.linspace(0, ymax, nb_points)
    
    X1 , Y1  = np.meshgrid(x,y)                       # create a grid
    DX1, DY1 = fish([X1, Y1])                      # compute growth rate on the gridt
    M = (np.hypot(DX1, DY1))                           # Norm of the growth rate 
    M[ M == 0] = 1.                                 # Avoid zero division errors 
    DX1 /= M                                        # Normalize each arrow
    DY1 /= M

    def iso_x(y):
        return ((y-y)+d/(a*(c-h*d))) # I'm pulling a trick here with y, it's sloppy coding to get an array out
    def iso_y(x):
        return (b*(1+a*h*x)*(1-x/K)/a)
    iso1 = iso_x(y)
    iso2 = iso_y(x)
    
    # Draw direction fields, using matplotlib 's quiver function
    # I choose to plot normalized arrows and to use colors to give information on
    # the growth speed
    p.title('Trajectories and direction fields')
    Q = p.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=p.cm.plasma)
    p.plot(iso1, y, c='black')
    p.plot(x, iso2, c='black')
    p.xlabel('Prey abundance')
    p.ylabel('Predator abundance')
    #p.legend(loc='lower right')
    p.grid()
    p.xlim(0, xmax)
    p.ylim(0, ymax)
    p.show()
    
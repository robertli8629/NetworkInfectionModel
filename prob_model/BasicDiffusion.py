import snap
from random import *
import matplotlib.pyplot as plt
import math
from dataLoader import loadGraphFromFile, loadFeature, loadFeatureName

def spread(G, infected, p_infect, p_recover):
    hasInfected = infected.copy()
    numInfected = [len(infected)]
    while len(infected) > 0:
        for key in infected.keys():
            ni = G.GetNI(key)
            deg = ni.GetOutDeg()
            for i in range(deg):
                n2i = ni.GetOutNId(i)
                if random() < p_infect and not n2i in hasInfected:
                    infected[n2i] = 1
                    hasInfected[n2i] = 1
        for key in infected.keys():
            if random() < p_recover:
                del infected[key]
        numInfected.append(len(infected))
    return (numInfected, hasInfected)


#features = loadFeature("../project/twitter/12831.feat")
#featName = loadFeatureName("../project/twitter/12831.featnames")

p_infect = 0.2
p_recover = 0.2
iters = 100

#Theoretical
H = 1
S = [1]
N = 236    # twitter
E = 2478   # twitter
#N = 333     # facebook
#E = 5038    # facebook
s = E / float(N*N)
#outs = s
while S[len(S)-1] > 0.1:
    lastS = S[len(S)-1]
    #newAdopt = (N-H)*(1-math.exp(-p_infect*outs))
    newAdopt = (N-H)*(1-math.exp(-p_infect*s*lastS))
    
    #p_deg = [1-(1-p_infect)**v for v in range(1,N)]
    #p_sum = sum(p_deg)
    #avg_deg = 0
    #for i in range(0,int(N-1)):
    #    avg_deg += p_deg[i]/p_sum*(i+1)
    
    #if N-H-newAdopt <= 0:
    #    outs = 0
    #else:
    #    print outs
    #    outs = (outs*(N-H)-newAdopt*avg_deg)/(N-H-newAdopt)+s*newAdopt
    S.append((1-p_recover)*(lastS+newAdopt))
    H += newAdopt
    #outs = (1-p_recover)*((1-p_infect)*outs + newAdopt * s)
print H
print sum(S)

ERSim_num_cum_infected = []
ERSim_num_hasInfected = 0
for count in range(0,iters):
    G = snap.GenRndGnm(snap.PNGraph, N, E)
    infected = {}
    infected[G.GetRndNId()] = 1
    num_infected, hasInfected = spread(G, infected, p_infect, p_recover)
    ERSim_num_hasInfected += len(hasInfected)
    for time in range(0, len(num_infected)):
        if time >= len(ERSim_num_cum_infected):
            ERSim_num_cum_infected.append(num_infected[time])
        else:
            ERSim_num_cum_infected[time] += num_infected[time]

ERSim_num_hasInfected /= float(iters)
ERSim_num_cum_infected = [v/float(iters) for v in ERSim_num_cum_infected]        
print ERSim_num_hasInfected
print sum(ERSim_num_cum_infected)

G = loadGraphFromFile("../project/twitter/12831.edges")
#G = loadGraphFromFile("../project/facebook/0.edges")
TwitterSim_num_cum_infected = []
TwitterSim_num_hasInfected = 0
for count in range(0,iters):
    infected = {}
    infected[G.GetRndNId()] = 1
    num_infected, hasInfected = spread(G, infected, p_infect, p_recover)
    TwitterSim_num_hasInfected += len(hasInfected)
    for time in range(0, len(num_infected)):
        if time >= len(TwitterSim_num_cum_infected):
            TwitterSim_num_cum_infected.append(num_infected[time])
        else:
            TwitterSim_num_cum_infected[time] += num_infected[time]

TwitterSim_num_hasInfected /= float(iters)
TwitterSim_num_cum_infected = [v/float(iters) for v in TwitterSim_num_cum_infected]        
print TwitterSim_num_hasInfected
print sum(TwitterSim_num_cum_infected)

#plt.plot(num_cum_infected, label="Number of infected nodes", S, label="aa")
plt.plot(range(0,len(S)),S,'r',label="ER Theory")
plt.plot(range(0,len(ERSim_num_cum_infected)),ERSim_num_cum_infected,'g',label="ER Simulation")
plt.plot(range(0,len(TwitterSim_num_cum_infected)),TwitterSim_num_cum_infected,'b',label="Twitter Simulation")


plt.xlabel('time')
plt.ylabel('infected number')
plt.legend()
plt.show()

import snap
from random import *
import matplotlib.pyplot as plt
import math
import operator
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
            if random() < p_recover * 16 / (G.GetNI(key).GetInDeg() + 1.0):
            #if random() < p_recover:
                del infected[key]
        numInfected.append(len(infected))
    return (numInfected, hasInfected)

def spreadAvg(G, infected, p_infect, p_recover, iters):
    cum_infected = 0
    for count in range(0,iters):
        num_infected, hasInfected = spread(G, infected.copy(), p_infect, p_recover)
        cum_infected += sum(num_infected)
    return float(cum_infected) / iters

def topDegreeNodes(G, k):
    MaxDegV = snap.TIntFltPrV()
    for NI in G.Nodes():
        degree = NI.GetOutDeg()
        item = snap.TIntFltPr(NI.GetId(), degree)
        if MaxDegV.Len() == 0:
            MaxDegV.Ins(0, item)
            continue
        for i in range(0, MaxDegV.Len()):
            if item.GetVal2() > MaxDegV[i].GetVal2():
                MaxDegV.Ins(i, item)
                break
        if MaxDegV.Len() > k:
            MaxDegV.Del(MaxDegV.LastValN())
    return MaxDegV
  

p_infect = 0.05
p_recover = 0.3
iters = 400
large_iters = 10000
set_num = 8
G = loadGraphFromFile("../project/twitter/12831.edges")

# Greedy
greedy_infect_time = [0]*(set_num+1)
upper_bound = [0]*(set_num+1)
greedy_init_set = {}
max_pot_increase = {}
for node in G.Nodes():
    max_pot_increase[node.GetId()] = 1e8
sorted_pot_increase = sorted(max_pot_increase.items(), key=operator.itemgetter(1), reverse=True)

for i in range(1, set_num+1):
    max_time = greedy_infect_time[i-1]
    max_increase = 0
    max_id = -1
    for nodeid, increase in sorted_pot_increase:
        if increase <= max_increase or nodeid in greedy_init_set:
            continue
        init_set = greedy_init_set.copy()
        init_set[nodeid] = 1
        infect_time = spreadAvg(G, init_set, p_infect, p_recover, iters)
        max_pot_increase[nodeid] = infect_time - greedy_infect_time[i-1]
        if infect_time > max_time:
            max_time = infect_time
            max_increase = infect_time - greedy_infect_time[i-1]
            max_id = nodeid
    greedy_infect_time[i] = max_time

    # Compute upper bound
    sorted_pot_increase = sorted(max_pot_increase.items(), key=operator.itemgetter(1), reverse=True)
    upper_bound[i] = greedy_infect_time[i-1]
    tau_num = 0
    for nodeid, increase in sorted_pot_increase:
        if tau_num == i:
            break
        if not nodeid in greedy_init_set:
            tau_num +=1
            upper_bound[i] += increase
    # Modify initial set
    if max_id >= 0:
        greedy_init_set[max_id] = 1
naive_bound = [val/0.63212 for val in greedy_infect_time]

# Random
random_infect_time = [0]*(set_num+1)
random_init_set = {}
for i in range(1, set_num+1):
    new_node_id = G.GetRndNId()
    while new_node_id in random_init_set:
        new_node_id = G.GetRndNId()
    random_init_set[new_node_id] = 1
    random_infect_time[i] = spreadAvg(G, random_init_set, p_infect, p_recover, large_iters)

# Degree
MaxDegV = topDegreeNodes(G, set_num)
degree_infect_time = [0]*(set_num+1)
degree_init_set = {}
for i in range(1, set_num+1):
    item = MaxDegV[i-1]
    degree_init_set[item.GetVal1()] = 1
    degree_infect_time[i] = spreadAvg(G, degree_init_set, p_infect, p_recover, large_iters)


plt.plot(range(0,set_num+1),greedy_infect_time,'r',label="Greedy")
plt.plot(range(0,set_num+1),random_infect_time,'g',label="Random")
plt.plot(range(0,set_num+1),degree_infect_time,'b',label="Degree")
plt.plot(range(0,set_num+1),upper_bound,'c',label="Data Upper Bound")
plt.plot(range(0,set_num+1),naive_bound,'m',label="Naive Upper Bound")

plt.xlabel('Initial set number')
plt.ylabel('Cumulative infected time')
plt.legend(loc=4)
plt.show()

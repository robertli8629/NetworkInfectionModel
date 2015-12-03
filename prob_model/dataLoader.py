import snap
from random import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def printStats(G):
	print "number of nodes in G: ", G.GetNodes()
	print "number of edges in G: ", G.GetEdges()


def loadGraphFromFile(filename):
	nodes = {}
	G = snap.TNGraph.New()
	f = open(filename)
	for line in f.readlines():
		# print line
		lst = line.strip().split()
		n1 = int(lst[0])
		n2 = int(lst[1])
		if n1 not in nodes:
			nodes[n1] = 1
			G.AddNode(n1)
		if n2 not in nodes:
			nodes[n2] = 1
			G.AddNode(n2)
		G.AddEdge(n1, n2)

	f.close()
	return G


def loadFeature(filename):
	d = {}
	f = open(filename)
	for line in f.readlines():
		# print line
		lst = line.strip().split()
		n1 = int(lst[0])
		leng = len(lst)
		d[n1] = []
		for i in range(1, leng):
			if lst[i] == "1":
				d[n1].append(i)

	f.close()
	return d

def loadFeatureName(filename):
	ret = []
	f = open(filename)
	for line in f.readlines():
		# print line
		lst = line.strip().split()
		n1 = int(lst[0])
		tag = lst[1]
		ret.append(tag)

	f.close()
	return ret


G = loadGraphFromFile("../data/twitter/12831.edges")
features = loadFeature("../data/twitter/12831.feat")
# print features

featName = loadFeatureName("../data/twitter/12831.featnames")
# print featName

printStats(G)

infected = {}
cleared = {}

def infect(n, infected, cleared, prob):
	if n in cleared or n in infected:
		return
	if random() < prob:
		infected[n] = 1

def clear(n, infected, cleared, prob):
	if n in cleared or n not in infected:
		return
	if random() < prob:
		del infected[n]
		cleared[n] = 1

i = randint(0, len(features) - 1);

infected[features.keys()[i]] = 1

print infected

p_infect = 0.1
p_clear = 0.01
dp_infect = 0.95
dp_clear = 1.05

def update_p_infect():
	return p_infect * dp_infect

def update_p_clear():
	if p_clear < 0.5:
		return p_clear * dp_clear
	else:
		return 1-(1/p_clear-1)*0.5

iters = 50
num_infected = []
for it in range(iters):
	for e in infected.keys():
		ni = G.GetNI(e)
		deg = ni.GetOutDeg()
		for i in range(deg):
			n2i = ni.GetOutNId(i)
			infect(n2i, infected, cleared, p_infect)
	for e in infected.keys():
		clear(e, infected, cleared, p_clear)
	# update prob
	p_infect = update_p_infect()
	p_clear = update_p_clear()

	print len(infected), p_infect, p_clear
	num_infected.append(len(infected))


isPlot = False
isPlot = True
if isPlot:
	plt.plot(num_infected, label="label")
	plt.xlabel('k')
	plt.ylabel('q_k')
	plt.legend()
	plt.show()



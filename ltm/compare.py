import model
import sys
import matplotlib.pyplot as plt
import random
from operator import add

adjlist = {}
with open(sys.argv[1], 'r') as f:
	for line in f:
		src, dst, weight = line.split(',')
		if dst not in adjlist:
			adjlist[dst] = {}
		adjlist[dst][src] = float(weight)

topDegreeNodes = []
with open('nodes_sorted_by_degree', 'r') as f:
	for line in f:
		node, _ = line.split()
		topDegreeNodes.append(node)

topInfluenceNodes = []
influences = []
with open('nodes_sorted_by_influence', 'r') as f:
	for line in f:
		node, influence = line.split()
		influences.append((float(influence), node))
		topInfluenceNodes.append(node)

def compare(adjlist, threshold, trigger, low, high, size, times, debug=True):
	defaultThresholds = {}
	defaultTriggers = {}
	for node in adjlist:
		defaultThresholds[node] = threshold
		defaultTriggers[node] = trigger
	defaultTime = 30

	degree = [0] * (defaultTime + 1)
	influence = [0] * (defaultTime + 1)
	integratedInfluence = [0] * (defaultTime + 1)
	for _ in range(times):
		activeness = {}
		for node in adjlist:
			activeness[node] = [1.0] * random.randint(low, high)
		integratedInfluences = map(lambda x: (x[0] * sum(activeness[x[1]]), x[1]), influences)
		topIntegratedInfluenceNodes = map(lambda x: x[1], sorted(integratedInfluences, reverse=True))

		ltm = model.LTM(adjlist, defaultThresholds, activeness, defaultTriggers)

		activeNodes = ltm.simulate(defaultTime, topDegreeNodes[:size])
		for i, x in enumerate(activeNodes):
			degree[i] += x

		activeNodes = ltm.simulate(defaultTime, topInfluenceNodes[:size])
		for i, x in enumerate(activeNodes):
			influence[i] += x

		activeNodes = ltm.simulate(defaultTime, topIntegratedInfluenceNodes[:size])
		for i, x in enumerate(activeNodes):
			integratedInfluence[i] += x

	degree = map(lambda x: x / float(times), degree)
	influence = map(lambda x: x / float(times), influence)
	integratedInfluence = map(lambda x: x / float(times), integratedInfluence)

	if debug:
		print sum(degree)
		print sum(influence)
		print sum(integratedInfluence)

		plt.plot(degree, label=('Top degree nodes'))
		plt.plot(influence, label=('Top influence nodes'))
		plt.plot(integratedInfluence, label=('Top integrated influence nodes'))
		plt.xlabel('time')
		plt.ylabel('# active nodes')
		plt.legend()
		plt.grid(True)
		plt.show()
	else:
		return (sum(degree), sum(influence), sum(integratedInfluence))

# compare(adjlist, 0.3, 1, 5, 15, 50, 10)

# thresholds = map(lambda x: x * 0.1, range(1, 9))
# degree = []
# influence = []
# integratedInfluence = []
# for threshold in thresholds:
# 	res = compare(adjlist, threshold, 1, 5, 15, 10, 10, debug=False)
# 	degree.append(res[0])
# 	influence.append(res[1])
# 	integratedInfluence.append(res[2])

# plt.plot(thresholds, degree, label=('Top degree nodes'))
# plt.plot(thresholds, influence, label=('Top influence nodes'))
# plt.plot(thresholds, integratedInfluence, label=('Top integrated influence nodes'))
# plt.xlabel('threshold')
# plt.ylabel('# integrated active nodes')
# plt.legend()
# plt.grid(True)
# plt.show()

initset_sizes = map(lambda x: x * 10, range(1, 10))
degree = []
influence = []
integratedInfluence = []
for size in initset_sizes:
	res = compare(adjlist, 0.2, 1, 5, 15, size, 10, debug=False)
	degree.append(res[0])
	influence.append(res[1])
	integratedInfluence.append(res[2])

plt.plot(initset_sizes, degree, label=('Top degree nodes'))
plt.plot(initset_sizes, influence, label=('Top influence nodes'))
plt.plot(initset_sizes, integratedInfluence, label=('Top integrated influence nodes'))
plt.xlabel('init set size')
plt.ylabel('# integrated active nodes')
plt.legend(loc='upper left')
plt.grid(True)
plt.show()

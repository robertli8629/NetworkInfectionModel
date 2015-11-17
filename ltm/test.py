import model
import sys
import matplotlib.pyplot as plt

# Adjacency list are in the form {node: {neighbor: influence}}
# Here neighbors are nodes that pointing the current node
adjlist = {}

# Read edge list and generate the graph
with open(sys.argv[1], 'r') as f:
	if len(sys.argv) > 2 and sys.argv[2] == '-d':
		directed = True
	else:
		directed = False
	for line in f:
		src, dst = line.split()
		if src not in adjlist:
			adjlist[src] = {}
		adjlist[src][dst] = 0
		if not directed:
			if dst not in adjlist:
				adjlist[dst] = {}
			adjlist[dst][src] = 0

# Normalize influence
for node in adjlist:
	total = 0
	neighbors = set(adjlist[node].keys())
	for neighbor in neighbors:
		adjlist[node][neighbor] = len(neighbors & set(adjlist[neighbor].keys()))
		total += adjlist[node][neighbor]
	if total > 0:
		for neighbor in adjlist[node]:
			adjlist[node][neighbor] /= float(total)

# Default parameters configuration
influencers = sorted([(len(adjlist[node]), node) for node in adjlist], reverse=True)

defaultThresholds = {}
defaultActiveness = {}
defaultTriggers = {}
for node in adjlist:
	defaultThresholds[node] = 0.1
	defaultActiveness[node] = [1.0] * 10
	defaultTriggers[node] = 1

defaultTime = 100
defaultInfluencers = 10

fig = plt.figure(1)
fig.subplots_adjust(hspace=.3)

# Different thresholds
plt.subplot(221)
samples = map(lambda x: x * 0.1, range(1, 6))
for val in samples:
	thresholds = {}
	for node in adjlist:
		thresholds[node] = val
	ltm = model.LTM(adjlist, thresholds, defaultActiveness, defaultTriggers)
	activeNodes = ltm.simulate(defaultTime, set(map(lambda x: x[1], influencers[:defaultInfluencers])))
	plt.plot(activeNodes, label=('threshold = %f' % val))

plt.xlabel('time')
plt.ylabel('# active nodes')
plt.legend()
plt.grid(True)
plt.title('(a)')

# Different activeness
plt.subplot(222)
samples = xrange(2, 12, 2)
for val in samples:
	activeness = {}
	for node in adjlist:
		activeness[node] = [1.0] * val
	ltm = model.LTM(adjlist, defaultThresholds, activeness, defaultTriggers)
	activeNodes = ltm.simulate(defaultTime, set(map(lambda x: x[1], influencers[:defaultInfluencers])))
	plt.plot(activeNodes, label=('active time = %d' % val))

plt.xlabel('time')
plt.ylabel('# active nodes')
plt.legend()
plt.grid(True)
plt.title('(b)')

# Different number of influencers
plt.subplot(223)
samples = xrange(5, 35, 5)
for val in samples:
	ltm = model.LTM(adjlist, defaultThresholds, defaultActiveness, defaultTriggers)
	activeNodes = ltm.simulate(defaultTime, set(map(lambda x: x[1], influencers[:val])))
	plt.plot(activeNodes, label=('# influencers = %d' % val))

plt.xlabel('time')
plt.ylabel('# active nodes')
plt.legend()
plt.grid(True)
plt.title('(c)')

# Different number of influencers
plt.subplot(224)
samples = range(1, 5)
for val in samples:
	triggers = {}
	for node in adjlist:
		triggers[node] = val
	ltm = model.LTM(adjlist, defaultThresholds, defaultActiveness, triggers)
	activeNodes = ltm.simulate(defaultTime, set(map(lambda x: x[1], influencers[:defaultInfluencers])))
	plt.plot(activeNodes, label=('activation bound = %d' % val))

plt.axis([0, 80, 0, 350])
plt.xlabel('time')
plt.ylabel('# active nodes')
plt.legend()
plt.grid(True)
plt.title('(d)')

plt.show()


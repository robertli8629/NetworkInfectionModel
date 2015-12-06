import sys

adjlist = {}
with open(sys.argv[1], 'r') as f:
	for line in f:
		src, dst, weight = line.split(',')
		if src not in adjlist:
			adjlist[src] = {}
		adjlist[src][dst] = float(weight)

highDegree = sorted([(len(adjlist[node]), node) for node in adjlist], reverse=True)
with open('nodes_sorted_by_degree', 'w') as f:
	for node in highDegree:
		f.write('%s %d\n' % (node[1], node[0]))

highInfluence = sorted([(sum(adjlist[node].values()), node) for node in adjlist], reverse=True)
with open('nodes_sorted_by_influence', 'w') as f:
	for node in highInfluence:
		f.write('%s %f\n' % (node[1], node[0]))
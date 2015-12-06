import sys
from os import listdir

adjlist = {}
path = sys.argv[1]
directed = False
if len(sys.argv) > 2 and sys.argv[2] == '-d':
	directed = True
for filename in listdir(path):
	if filename[-5:] == 'edges':
		ego = filename[:-6]
		if ego not in adjlist:
			adjlist[ego] = {}
		with open(path + filename, 'r') as f:
			for line in f:
				src, dst = line.split()
				if src not in adjlist:
					adjlist[src] = {}
				adjlist[src][dst] = 0
				adjlist[ego][src] = 0
				adjlist[ego][dst] = 0
				if not directed:
					adjlist[src][ego] = 0
					if dst not in adjlist:
						adjlist[dst] = {}
					adjlist[dst][ego] = 0
					adjlist[dst][src] = 0

for node in adjlist:
	total = 0
	neighbors = set(adjlist[node].keys())
	for neighbor in neighbors:
		neighborFollows = set(adjlist[neighbor].keys()) if neighbor in adjlist else set()
		adjlist[node][neighbor] = len(neighbors & neighborFollows)
		total += adjlist[node][neighbor]
	if total > 0:
		for neighbor in adjlist[node]:
			adjlist[node][neighbor] /= float(total)

graph = open(path + 'graph.gdf', 'w')
weighted = open(path + 'weighted.edges', 'w')

graph.write('nodedef>name\n')
for node in adjlist:
	graph.write(node + '\n')
graph.write('edgedef>node1,node2,weight DOUBLE\n')

for node in adjlist:
	for neighbor in adjlist[node]:
		edge = ','.join([neighbor, node, str(adjlist[node][neighbor])]) + '\n'
		graph.write(edge)
		weighted.write(edge)

graph.close()
weighted.close()
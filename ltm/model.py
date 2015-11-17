import snap
import matplotlib.pyplot as plt

class LTM(object):
	# Adjacency list are in the form {node: {neighbor: influence}}
	# Here neighbors are nodes that pointing the current node
	def __init__(self, adjlist, thresholds, activeness, triggers):
		self.adjlist = adjlist
		self.thresholds = thresholds
		self.activeness = activeness
		self.triggers = triggers
		self.nodes = set(adjlist.keys())

	def simulate(self, time, initSet):
		activeNodes = []
		triggers = {}
		activelevel = {}
		for node in self.nodes:
			triggers[node] = 0
			activelevel[node] = -1
		for node in initSet:
			if triggers[node] < self.triggers[node]:
				triggers[node] += 1
				activelevel[node] = 0
		activeNodes.append(len(initSet))

		while time > 0:
			influence = {}
			for node in self.nodes:
				influence[node] = 0.0
				for neighbor in self.adjlist[node]:
					if activelevel[neighbor] >= 0:
						activeness = self.activeness[neighbor][activelevel[neighbor]]
						influence[node] += activeness * self.adjlist[node][neighbor]
			totalActiveNodes = 0
			for node in self.nodes:
				if activelevel[node] >= 0:
					if activelevel[node] == len(self.activeness[node]) - 1:
						activelevel[node] = -1
					else:
						activelevel[node] += 1
						totalActiveNodes += 1
				else:
					if influence[node] >= self.thresholds[node] and triggers[node] < self.triggers[node]:
						triggers[node] += 1
						activelevel[node] = 0
						totalActiveNodes += 1
			activeNodes.append(totalActiveNodes)
			if totalActiveNodes == 0:
				break
			time -= 1

		return activeNodes
		
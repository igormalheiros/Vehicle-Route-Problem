from VRPTW import Request

class readInput:
	
	def __init__(self, path):
		self.txt = open(path)
	def __str__(self):
		return "File: \n %s" % self.txt.read()

	def buildGraph(self):
		graph = {}
		t = self.txt.readlines()
		for line in t:
			(source,target, cost) = line.split()
			graph[(source,target)] = float(cost)
		return graph

	def buildRequests(self):
		requests = []
		t = self.txt.readlines()
		i = 1
		for line in t:
			(source, target, eStart, lStart, eEnd, lEnd) = line.split()
			requests.append(Request(i, source, target, float(eStart), float(lStart), float(eEnd), float(lEnd)))
			i = i + 1
		return requests

	def buildCarsPositions(self):
		return self.txt.read().split()

from VRPTW import *

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


	def buildSimpleRequests(self):
		requests = []
		t = self.txt.readlines()
		i = 1
		for line in t:
			(source, target, eStart, eEnd, capacity) = line.split()
			requests.append(SimpleRequest(i, source, target, float(eStart), float(eEnd), int(capacity)))
			i += 1
		requests.sort(key=lambda x : x.eStart)
		return requests

	def buildRequests(self):
		requests = []
		t = self.txt.readlines()
		i = 1
		for line in t:
			(source, target, eStart, lStart, eEnd, lEnd) = line.split()
			requests.append(Request(i, source, target, float(eStart), float(lStart), float(eEnd), float(lEnd)))
			i += 1

		return requests

	def buildCarsPositions(self):
		cars = []
		i = 1
		t = self.txt.readlines()
		for line in t:
			(position, capacity) = line.split()
			cars.append(Car(i,position, capacity))
			i += 1
		return cars

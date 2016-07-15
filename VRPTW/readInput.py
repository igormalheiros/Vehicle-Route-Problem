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
			eStart = eStart.split(":")
			eEnd = eEnd.split(":")
			eStart = int(eStart[0])*60 + int(eStart[1])
			eEnd = int(eEnd[0])*60 + int(eEnd[1])

			requests.append(SimpleRequest(i, source, target, eStart, eEnd, int(capacity)))
			i += 1
		requests.sort(key=lambda x : x.eStart)
		return requests

	def buildRequests(self):
		requests = []
		t = self.txt.readlines()
		i = 1
		for line in t:
			(source, target, eStart, lStart, eEnd, lEnd, passangers) = line.split()
			eStart = eStart.split(":")
			lStart = lStart.split(":")
			eEnd = eEnd.split(":")
			lEnd = lEnd.split(":")
			eStart = int(eStart[0])*60 + int(eStart[1])
			lStart = int(lStart[0])*60 + int(lStart[1])
			eEnd = int(eEnd[0])*60 + int(eEnd[1])
			lEnd = int(lEnd[0])*60 + int(lEnd[1])
			requests.append(Request(i, source, target, float(eStart), float(lStart), float(eEnd), float(lEnd), int(passangers)))
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

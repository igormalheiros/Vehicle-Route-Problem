from readInput import readInput
from VRPTW import *
import random

def generateCars(graph, n):
	return [Car(i, random.choice(graph.keys())[0], random.randint(4,8)) for i in range(1,n+1)]

def generateRequests(graph, n):
	requests = []
	for i in range(1, n+1):
		route = random.choice(graph.keys())
		startTime = random.randrange(8*60,20*60,60)
		requests.append(SimpleRequest(i, route[0], route[1], startTime, startTime+(graph[route]), random.randint(1,8)))

	return requests
graphFile = readInput("IrelandGraph.txt")
graph = graphFile.buildGraph()

cars = generateCars(graph, 20)
requests = generateRequests(graph, 50)
for c in cars:
	print(c)
for r in requests:
	print(r)
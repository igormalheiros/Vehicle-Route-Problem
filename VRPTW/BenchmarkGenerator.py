from readInput import readInput
from VRPTW import *
import random

def generateCars(graph, n):
	return [Car(i, random.choice(graph.keys())[0], random.randint(4,8)) for i in range(1,n+1)]

def generateRequests(graph, n):
	requests = []
	for i in range(1, n+1):
		route = random.choice(graph.keys())
		extraTime = random.randrange(0,300)
		eStart = random.randrange(8*60,20*60,60)
		lStart = eStart + random.randrange(0,180)
		eEnd = eStart+(graph[route])+ extraTime
		lEnd = (lStart + graph[route] + extraTime) + random.randrange(0,180)

		requests.append(Request(i, route[0], route[1], eStart, lStart, eEnd, lEnd, extraTime, random.randint(1,8)))

	return requests

graphFile = readInput("IrelandGraph.txt")
graph = graphFile.buildGraph()

#cars = generateCars(graph, 400)
requests = generateRequests(graph, 500)
#for c in cars:
#	print(c)

for r in requests:
	print(r)
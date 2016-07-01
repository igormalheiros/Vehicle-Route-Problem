from copy import deepcopy
from VRPTW import *
from sets import Set
from readInput import readInput
from GA import GA

def initialize():
	return deepcopy(carPos)

def checkTimeWindow(req, cost):
	return (req.eStart + cost == req.eEnd)
	
def objFunction(string):

	cars = initialize()

	#split the requests by each car
	assigns = {}
	for i in xrange(len(string)):
		if(string[i] in assigns):
			assigns[string[i]].append(requests[i])
		else:
			assigns[string[i]] = [requests[i]]

	score = 1
	for c in assigns:
		timeStart = 0
		for r in assigns[c]:
			#Check if the car is in the correct position on time and if it is possible reach the endLocation in time
			if ( (r.startLocation == cars[c-1].position) and
				 (checkTimeWindow(r, graph[(r.startLocation, r.endLocation)])) and
				 (timeStart <= r.eStart) and
				 (r.passengers <= cars[c-1].capacity)):

				score = score + 1
				timeStart = r.eEnd
				cars[c-1].position = r.endLocation

	return score

def measure(string):
	cars = initialize()

	#split the requests by each car
	assigns = {}
	for i in xrange(len(string)):
		if(string[i] in assigns):
			assigns[string[i]].append(requests[i])
		else:
			assigns[string[i]] = [requests[i]]

	decline = []
	accepted = {key: [] for key in string}

	for c in assigns:
		timeStart = 0
		for r in assigns[c]:
			#Check if the car is in the correct position on time and if it is possible reach the endLocation in time
			if ( (r.startLocation == cars[c-1].position) and
				 (checkTimeWindow(r, graph[(r.startLocation, r.endLocation)])) and
				 (timeStart <= r.eStart) and
				 (r.passengers <= cars[c-1].capacity) ):

				timeStart = r.eEnd
				cars[c-1].position = r.endLocation
				accepted[c].append(r)
			else:
				decline.append(r)

	return(cars,accepted,decline)

#Cars starts posistions, graph and request files

carsFile = readInput("20cars.txt")
graphFile = readInput("IrelandGraph.txt")
requestsFile = readInput("50requests.txt")
graph = graphFile.buildGraph()
requests = requestsFile.buildSimpleRequests()
carPos = carsFile.buildCarsPositions()
for r in requests:
	print(r)
#GA parameters
nReq = len(requests)
population = 200
breeds = 600
variability = len(carPos)
mutation = 0.3
copyFraction = 0.6

#run GA

test = GA(nReq, population, breeds, variability, mutation, copyFraction, objFunction)
best = test.run()

#Outputs
print("\n>>>> BEST ASSIGMENT <<<< \n%s" % best)
(cars, accepteds, declines) = measure(best)

print("\n>>>> CARS FINAL POSITIONS <<<<\n")
for c in cars:
	print("%d in position %s" % (c.indx, c.position))

print("\n>>>> ACCEPTED REQUISITIONS <<<<\n")
for c in accepteds:
	for acc in accepteds[c]:
		print("%s was possible to car %s" % (acc,c))


print("\n>>>> NOT ACCEPTED REQUISITIONS <<<<\n")
for d in declines:
	print("%s was not possible" % d)
print("\nTotal of accepted requisitions: %d/%d" % ((len(best)-len(declines)), len(best)))
print("Cars used %s %d/%d" % (Set(best), len(Set(best)), len(carPos)) )



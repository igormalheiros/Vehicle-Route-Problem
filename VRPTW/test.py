from copy import deepcopy
from VRPTW import *
from sets import Set
from readInput import readInput
from GA import GA

def initialize():
	return deepcopy(carPos)

def shrinkByFeasible(accepteds):
	for car in accepteds:
		for i in range(len(accepteds[car])):
			current = accepteds[car][i]
			cost = graph[(current.startLocation, current.endLocation)]

			#the earliest timeEnd is at least the earliest timeStart + cost
			accepteds[car][i].eEnd =   max(accepteds[car][i].eEnd, accepteds[car][i].eStart+cost)
			accepteds[car][i].eStart = max(accepteds[car][i].eEnd-cost, accepteds[car][i].eStart)

	return accepteds
def shrinkByIntersection(accepteds):

	#Look for intersection between fallowed requisitions and shrink the time table in order to attend both
	for car in accepteds:
		for i in range(len(accepteds[car])):
			if( (i+1) < (len(accepteds[car])) ):
				current = deepcopy(accepteds[car][i])
				next = deepcopy(accepteds[car][i+1])
				cost = graph[(current.startLocation, current.endLocation)]

				current.eEnd = next.eStart = max(current.eEnd, next.eStart)
				current.lEnd = next.lStart = min(current.lEnd, next.lStart)

				#CHECK IF MAKE SENSE!!!!!
				if( checkTimeWindow(current, cost)):
					accepteds[car][i] = deepcopy(current)
				if( checkTimeWindow(next, cost)):
					accepteds[car][i+1] = deepcopy(next)
	return accepteds

def shrinkTimeWindow(accepteds):
	return (shrinkByFeasible(shrinkByIntersection(shrinkByFeasible(accepteds))))

def checkTimeWindow(req, cost):
	eStart = req.eStart
	lStart = req.lStart
	eEnd = req.eEnd
	lEnd = req.lEnd

	return (  ( (eStart+cost) <= eEnd <= (lStart+cost) ) or
			  ( (eStart+cost) <= lEnd <= (lStart+cost) )  or
			  ( eEnd <= (eStart+cost) <= lEnd) or
			  ( eEnd <= (lStart+cost) <= lEnd) )

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
				 (timeStart <= r.lStart) ):

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
				 (timeStart <= r.eStart) ):

				timeStart = r.eEnd
				cars[c-1].position = r.endLocation
				accepted[c].append(r)
			else:
				decline.append(r)

	accepted = shrinkTimeWindow(accepted)
	return(cars,accepted,decline)

#Cars starts posistions, graph and request files

carsFile = readInput("CarsPositions.txt")
graphFile = readInput("IrelandGraph.txt")
requestsFile = readInput("Requests.txt")
graph = graphFile.buildGraph()
requests = requestsFile.buildRequests()
carPos = carsFile.buildCarsPositions()

#GA parameters
nReq = len(requests)
population = 10
breeds = 200
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

print(checkTimeWindow(Request(1,'a', 'b', 8, 9, 10, 10), 0.5))
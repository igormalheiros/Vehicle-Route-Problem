from copy import deepcopy
from VRPTW import *
from sets import Set
from readInput import readInput
from GA import GA

def initialize():
	return deepcopy(carPos)

def isOverlap(req1, req2):
	return ( (req2.eStart <= req1.eEnd <= req2.lStart) or
			 (req2.eStart <= req1.lEnd <= req2.lStart) or
			 ((req1.eEnd <= req2.eStart <= req1.lEnd)) or
			 ((req1.eEnd <= req2.lStart <= req1.lEnd)) )

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
			if( (i+1) < (len(accepteds[car])) and isOverlap(accepteds[car][i],accepteds[car][i+1]) ):
				current = deepcopy(accepteds[car][i])
				next = deepcopy(accepteds[car][i+1])
				cost = graph[(current.startLocation, current.endLocation)]

				current.eEnd = next.eStart = max(current.eEnd, next.eStart)
				current.lEnd = next.lStart = min(current.lEnd, next.lStart)

				#CHECK IF MAKE SENSE!!!!!
				if( checkTimeWindow(current, cost) ):
					accepteds[car][i] = deepcopy(current)
				if ( checkTimeWindow(next, cost) ):
					accepteds[car][i+1] = deepcopy(next)
					
	return accepteds

def shrinkTimeWindow(accepteds):
	return (shrinkByFeasible(shrinkByIntersection(accepteds)))

def checkTimeWindow2(req, cost):
	return ( abs(req.eEnd-req.eStart) >= cost)

def checkTimeWindow(req, cost):
	eStart = req.eStart
	lStart = req.lStart
	eEnd = req.eEnd
	lEnd = req.lEnd

	return ( ( eEnd <= (eStart+cost) <= lEnd) or
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
				 (timeStart <= r.lStart) and
				 (int(r.passengers) <= int(cars[c-1].capacity)) ):

				score = score + 1
				cars[c-1].position = r.endLocation

				if ( (r.eStart < timeStart) and 
				     (r.eEnd <= (timeStart+graph[(r.startLocation, r.endLocation)]) <= r.lEnd) ):

					timeStart += graph[(r.startLocation, r.endLocation)]

				else:
					timeStart = r.eEnd

	return score

def measure(string):
	cars = initialize()
	carsRoute = {key.indx:[] for key in cars}

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
			if ( ( r.startLocation == cars[c-1].position) and
				 ( checkTimeWindow(r, graph[(r.startLocation, r.endLocation)])) and
				 ( timeStart <= r.lStart) and
				 ( int(r.passengers) <= int(cars[c-1].capacity))):

				cars[c-1].position = r.endLocation
				accepted[c].append(r)
				carsRoute[c].append(r)

				if ( (r.eStart < timeStart) and 
				   (r.eEnd <= (timeStart+graph[(r.startLocation, r.endLocation)]) <= r.lEnd) ):

					timeStart += graph[(r.startLocation, r.endLocation)]
					
				else:
					timeStart = r.eEnd

			else:
				decline.append(r)

	#accepted = shrinkTimeWindow(accepted)
	return(carsRoute,accepted,decline)

#Cars starts posistions, graph and request files

carsFile = readInput("20cars.txt")
graphFile = readInput("IrelandGraph.txt")
requestsFile = readInput("50requests.txt")
graph = graphFile.buildGraph()
requests = requestsFile.buildRequests()
carPos = carsFile.buildCarsPositions()

#GA parameters
nReq = len(requests)
population = 200
breeds = 600
variability = len(carPos)
mutation = 0.3
copyFraction = 0.3

dicHour = {key : 0 for key in xrange(8,20)}
dicDepart = {key[0]: 0 for key in graph.keys()}
dicArriv = {key[0]: 0 for key in graph.keys()}
dicPassagenrs = {key : 0 for key in xrange(1,9)}

for r in requests:
	dicHour[r.eStart/60] += 1
	dicDepart[r.startLocation] += 1
	dicPassagenrs[r.passengers] += 1
	dicArriv[r.endLocation] += 1

#run GA
test = GA(nReq, population, breeds, variability, mutation, copyFraction, objFunction)
best = [11, 3, 16, 15, 18, 17, 16, 15, 2, 5, 13, 6, 19, 1, 7, 9, 13, 5, 13, 8, 12, 5, 17, 7, 18, 2, 12, 14, 3, 2, 20, 20, 4, 12, 7, 20, 6, 15, 19, 4, 5, 4, 16, 2, 7, 1, 11, 10, 6, 19]
#best = [19, 3, 4, 6, 9, 3, 1, 7, 11, 12, 13, 6, 18, 16, 7, 19, 4, 6, 3, 12, 19, 20, 15, 14, 8, 7, 4, 18, 14, 9, 2, 1, 8, 18, 7, 14, 5, 6, 18, 20, 20, 10, 12, 10, 12, 13, 5, 1, 17, 1]
#Outputs

#Benchmark distribution
print("\n>>>> HOURS <<<<")
for k in dicHour.keys():
	print ("%d -> %d" % (k, dicHour[k]))

print("\n>>>> DEPARTURE <<<<")

for k in dicDepart.keys():
	print ("%s -> %d" % (k, dicDepart[k]))

print("\n>>>> ARRIVED <<<<")
for k in dicArriv.keys():
	print ("%s -> %d" % (k, dicArriv[k]))

print("\n>>>> PASSAENGERS <<<<")
for k in dicPassagenrs.keys():
	print ("%d -> %d" % (k, dicPassagenrs[k]))

#Best Results
print("\n>>>> BEST ASSIGMENT <<<< \n%s" % best)
(cars, accepteds, declines) = measure(best)

notUsed = 0
used = []
print("\n>>>> CARS TOURS <<<<\n")
for c in cars:
	print("*** CAR %d:" % c)
	if(cars[c] == []):
		notUsed += 1
	else:
		used.append(c)
	for r in cars[c]:
		print("Req %d: %s to %s" % (r.indx, r.startLocation, r.endLocation))
	print

print("\n>>>> ACCEPTED REQUISITIONS <<<<\n")
for c in accepteds:
	for acc in accepteds[c]:
		print("%s was possible to car %s" % (acc,c))


print("\n>>>> NOT ACCEPTED REQUISITIONS <<<<\n")
for d in declines:
	print("%s was not possible" % d)
print("\nTotal of accepted requisitions: %d/%d" % ((len(best)-len(declines)), len(best)))
print("Cars used %s %d/%d" % (Set(used), (len(carPos)-notUsed), len(carPos)) )

'''
Request 10: Kinsale to Limerick [18:00,20:35] [20:01,21:16] with 7 passengers was possible to car 5
Request 18: Limerick to Dingle [19:00,21:16] [21:23,21:39] with 5 passengers was possible to car 5'''

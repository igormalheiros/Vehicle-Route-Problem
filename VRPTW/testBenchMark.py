from copy import deepcopy
from VRPTW import *
from sets import Set
from readInput import readInput
from GA import GA

def initialize():
	return deepcopy(carPos)

def checkTimeWindow(req, cost):
	return ( abs(req.eEnd-req.eStart) >= cost)
	
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
				 (int(r.passengers) <= int(cars[c-1].capacity)) ):

				score = score + 1
				timeStart = r.eEnd
				cars[c-1].position = r.endLocation

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
			if ( (r.startLocation == cars[c-1].position) and
				(checkTimeWindow(r, graph[(r.startLocation, r.endLocation)])) and
				 ( timeStart <= r.eStart) and
				 ( int(r.passengers) <= int(cars[c-1].capacity))):

				timeStart = r.eEnd
				cars[c-1].position = r.endLocation
				accepted[c].append(r)
				carsRoute[c].append(r)
				
			else:
				decline.append(r)

	return(carsRoute,accepted,decline)

#Cars starts posistions, graph and request files

carsFile = readInput("20cars.txt")
graphFile = readInput("IrelandGraph.txt")
requestsFile = readInput("50requests2.txt")
graph = graphFile.buildGraph()
requests = requestsFile.buildSimpleRequests()
carPos = carsFile.buildCarsPositions()

i = 0
for r in requests:
	i += 1
	print("%d %s" % (i,r))

#GA parameters
nReq = len(requests)
population = 600
breeds = 1000
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
best = test.run()
#best = [16,17,4,10,11,1,1,14,3,6,9,7,15,1,17,18,16,1,2,1,10,14,1,7,20,19,16,15,1,1,1,3,1,1,5,15,1,1,9,20,8,12,1,1,1,11,15,4,12,1]
#best = [16, 6, 13, 10, 9, 11, 12, 4, 3, 17, 9, 16, 15, 6, 6, 14, 7, 13, 2, 18, 10, 1, 6, 16, 15, 19, 7, 20, 17, 7, 16, 12, 20, 2, 5, 18, 15, 11, 8, 13, 4, 3, 15, 1, 20, 7, 8, 17, 6, 12]
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

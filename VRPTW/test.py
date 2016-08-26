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
	w = req.extraTime

	return ( ( eEnd <= (eStart+cost+w) <= lEnd) or
			 ( eEnd <= (lStart+cost+w) <= lEnd) )

def objFunction(string):

	cars = initialize()

	#split the requests by each car
	assigns = {key:[] for key in xrange(1,variability+1)}

	for i in xrange(len(string)):
		assigns[string[i]].append(requests[i])

	score = 1
	for c in assigns:
		timeStart = 0
		for r in assigns[c]:
			#Check if the car is in the correct position on time and if it is possible reach the endLocation in time
			if ( (r.startLocation == cars[c-1].position) and
				 (checkTimeWindow(r, graph[(r.startLocation, r.endLocation)])) and
				 (timeStart <= r.lStart) and
				 (r.passengers <= cars[c-1].capacity) ):

				score += 1
				cars[c-1].position = r.endLocation

				if ( (r.eStart < timeStart) and 
				     (r.eEnd <= (timeStart+r.extraTime+graph[(r.startLocation, r.endLocation)]) <= r.lEnd) ):

					timeStart += graph[(r.startLocation, r.endLocation)] + r.extraTime

				else:
					timeStart = r.eEnd

	return score

def measure(string):
	cars = initialize()
	carsRoute = {key.indx:[] for key in cars}

	#split the requests by each car
	assigns = {key:[] for key in xrange(1,variability+1)}

	for i in xrange(len(string)):
		assigns[string[i]].append(requests[i])

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
				   (r.eEnd <= (timeStart+r.extraTime+graph[(r.startLocation, r.endLocation)]) <= r.lEnd) ):

					timeStart += (graph[(r.startLocation, r.endLocation)] + r.extraTime)
					
				else:
					timeStart = r.eEnd

			else:
				decline.append(r)

	#accepted = shrinkTimeWindow(accepted)
	return(carsRoute,accepted,decline)

#Cars starts posistions, graph and request files
#carsList = ["Tests/50Requests/10cars.txt","Tests/50Requests/20cars.txt","Tests/50Requests/30cars.txt","Tests/50Requests/40cars.txt"]
carsList = ["Tests/500Requests/400cars.txt"]
data = []

for p in carsList:
	for a in xrange(1):
		carsFile = readInput(p)
		graphFile = readInput("IrelandGraph.txt")
		requestsFile = readInput("Tests/500Requests/500requestsTimeWaste.txt")
		graph = graphFile.buildGraph()
		requests = requestsFile.buildRequests()
		carPos = carsFile.buildCarsPositions()


		for r in requests:
			print(r)
		#GA parameters
		nReq = len(requests)
		population = 50
		breeds = 10
		variability = len(carPos)
		mutation = 0.3
		copyFraction = 0.4

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
		#best = (0,[6, 6, 1, 2, 17, 7, 5, 5, 16, 14, 18, 5, 19, 10, 5, 20, 16, 10, 1, 5, 14, 16, 16, 1, 16, 4, 14, 18, 7, 9, 13, 15, 11, 18, 3, 20, 11, 7, 2, 6, 16, 15, 17, 11, 1, 5, 7, 19, 13, 10])
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
		print("\n>>>> BEST ASSIGMENT <<<< \n%s" % best[1])
		(cars, accepteds, declines) = measure(best[1])

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
		print("\nTotal of accepted requisitions: %d/%d" % ((len(best[1])-len(declines)), len(best[1])))
		print("Iteration: %d" % best[0])
		print("Cars used %s %d/%d" % (Set(used), (len(carPos)-notUsed), len(carPos)) )

		'''
		Request 10: Kinsale to Limerick [18:00,20:35] [20:01,21:16] with 7 passengers was possible to car 5
		Request 18: Limerick to Dingle [19:00,21:16] [21:23,21:39] with 5 passengers was possible to car 5'''
		data.append( (best[0], ((len(best[1])-len(declines)), len(best[1]))) )

for d in data:
	print("%s %s" % (d[0],d[1]) )
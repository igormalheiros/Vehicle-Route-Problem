from copy import deepcopy
from VRPTW import *
from sets import Set
from readInput import readInput
from GA import GA

def initialize():
	return deepcopy(carPos)

def checkTimeWindow(req, cost):
	return ( abs(req.eEnd-req.eStart) >= (cost+req.extraTime))
	
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
			if ( ( r.startLocation == cars[c-1].position) and
				 ( checkTimeWindow(r, graph[(r.startLocation, r.endLocation)])) and
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
carsList = ["Tests/500Requests/100cars.txt","Tests/500Requests/200cars.txt","Tests/500Requests/300cars.txt","Tests/500Requests/400cars.txt"]
data = []
for p in carsList:
	for a in xrange(5):
		carsFile = readInput(p)
		graphFile = readInput("IrelandGraph.txt")
		requestsFile = readInput("Tests/500Requests/500requestsTimeWaste.txt")
		graph = graphFile.buildGraph()
		requests = requestsFile.buildRequests()
		carPos = carsFile.buildCarsPositions()

		i = 0
		for r in requests:
			i += 1
			print("%d %s" % (i,r))

		#GA parameters
		nReq = len(requests)
		population = 500
		breeds = 4000
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
		#best = (0,[15, 16, 16, 20, 1, 2, 12, 1, 19, 18, 3, 14, 9, 7, 16, 2, 12, 16, 3, 14, 13, 7, 14, 6, 11, 4, 10, 14, 19, 13, 18, 17, 11, 20, 12, 2, 10, 15, 3, 6, 12, 17, 14, 6, 15, 9, 16, 9, 18, 7])
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

		data.append( (best[0], ((len(best[1])-len(declines)), len(best[1]))) )

for d in data:
	print("%s %s" % (d[0],d[1]) )
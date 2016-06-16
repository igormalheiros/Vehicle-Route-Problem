from VRPTW import *
from readInput import readInput
from GA import GA

def initialize():
	return [Car(i, carPos[i], 5) for i in xrange(len(carPos))]

def checkTimeWindow(req, cost):
	eStart = req.eStart
	lStart = req.lStart
	eEnd = req.eEnd
	lEnd = req.lEnd

	return ( ( (eStart+cost) <= eEnd <= (lStart+cost) ) or
			 ( (eStart+cost) <= lEnd <= (lStart+cost) )  or
			 ( eEnd <= (eStart+cost) <= lEnd) or
			 ( eEnd <= (lStart+cost) <= lEnd) )

def objFunction(string):
	cars = initialize()

	k = 0
	score = 1

	for r in string:
		carId = int(r)-1
		req = requests[k]
		#check if the car is in position of requisition and if it's possible to deleviry in latest time
		if(cars[carId].position == req.origin and
			checkTimeWindow(req, graph[(req.origin,req.destination)]) ):
			score = score + 1
			cars[carId].position = req.destination
		k = k+1

	return score

def wrongAssigment(string):
	cars = initialize()
	wrong = []
	k = 0
	for r in string:
		carId = int(r)-1
		req = requests[k]
		if(cars[carId].position == req.origin and
			checkTimeWindow(req, graph[(req.origin,req.destination)]) ):
			cars[carId].position = req.destination
		else:
			wrong.append(k+1)
		k = k + 1

	return wrong

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
cars = initialize()
wrongs = wrongAssigment(best)

print("\n>>>> CARS FINAL POSITIONS <<<<\n")
for c in cars:
	print("%d in position %s" % (c.indx, c.position))

print("\n>>>> NOT ACCEPTED REQUISITIONS <<<<\n")
for w in wrongs:
	print("Requisition %d was not possible" % w)
print("\nTotal of accepted requisitions: %d/%d" % ((len(best)-len(wrongs)), len(best)))

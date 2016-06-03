from GA import GA


class Request:
	def __init__(self, indx, origin, destination, eStart, lStart, eEnd, lEnd):
		self.indx = indx
		self.origin = origin
		self.destination = destination
		self.eStart = eStart
		self.lStart = lStart
		self.eEnd = eEnd
		self.lEnd = lEnd

	def __str__(self):
		return "Request %d: Origin -> %s Destination -> %s" % (self.indx, self.origin, self.destination)

class Car:
	def __init__(self, indx, position):
		self.indx = indx
		self.position = position

	def __str__(self):
		return "Car %d: Position -> %s" % (self.indx, self.position)

def initialize():
	return [Car(i, carPos[i]) for i in xrange(len(carPos))]

def checkTimeWindow(eStart, lStart, eEnd, lEnd, cost):
	return ( ( (eStart+cost)<= eEnd <= (lStart+cost) ) or
			 ( (eStart+cost)<= lEnd <= (lStart+cost) )  or
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
			checkTimeWindow(req.eStart, req.lStart, req.eEnd, req.lEnd, graph[req.origin][req.destination]) ):
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
			checkTimeWindow(req.eStart, req.lStart, req.eEnd, req.lEnd, graph[req.origin][req.destination]) ):
			cars[carId].position = req.destination
		else:
			wrong.append(k+1)
		k = k + 1

	return wrong
#Start variables
carPos = "AABCCDD"
#graph costs
graph = {'A' : {'B':   1, 'C':   1, 'D':   1},
		 'B' : {'A':   1, 'C': 2.5, 'D':   2},
		 'C' : {'A':   1, 'B': 2.5, 'D': 1.5},
		 'D' : {'A':   1, 'B':   2, 'C': 1.5}}
#requests
requests = [Request( 1, 'A', 'B',    8,    9,   10, 10.5), 
			Request( 2, 'C', 'A',    8,  8.5,   11, 11.5), 
			Request( 3, 'B', 'A',    9,   10,   10,   11), 
			Request( 4, 'D', 'C',  9.5, 10.5,   13,   15),
			Request( 5, 'D', 'A',  9.5,   10, 10.5,   12),
			Request( 6, 'A', 'B', 10.5, 11.5,   16, 17.5),
			Request( 7, 'A', 'C',   11,   12,   13,   14), 
			Request( 8, 'D', 'A',   11,   12,   16,   17),
			Request( 9, 'A', 'D', 11.5,   12, 12.5,   13),
			Request(10, 'B', 'C',   12,   14, 14.5,   15),
			Request(11, 'D', 'B',   12, 12.5,   15,   18),
			Request(12, 'B', 'D',   12, 12.5, 15.5,   16),
			Request(13, 'C', 'D', 12.5,   13,   14,   15),
			Request(14, 'C', 'A',   13,   15,   15,   17),
			Request(15, 'B', 'A',   13, 15.5,   15,   17),
			Request(16, 'D', 'C',   15,   16,   17,   18),
			Request(17, 'A', 'D',   16, 16.5, 17.5,   20),
			Request(18, 'C', 'B',   16, 16.5,   19,   21),
			Request(19, 'C', 'A',   19,   20, 20.5,   21),
			Request(20, 'A', 'B',   20,   22,   22, 23.5),]

nReq = 20
population = 150
breeds = 500
variability = 7
mutation = 0.3
copyFraction = 0.6

#For only 1 to 1 time Window
#print(objFunction("14167122414312412154"))

test = GA(nReq, population, breeds, variability, mutation, copyFraction, objFunction)
best = test.run()

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


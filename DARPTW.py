from GA import GA


class Request:
	def __init__(self, indx, origin, destination, eStart, eEnd, load):
		self.indx = indx
		self.origin = origin
		self.destination = destination
		self.eStart = eStart
		self.eEnd = eEnd
		self.load = load

	def __str__(self):
		return "Request %d: Origin -> %s Destination -> %s" % (self.indx, self.origin, self.destination)

class Car:
	def __init__(self, indx, position, capacity):
		self.indx = indx
		self.position = position
		self.capacity = capacity
		self.load = 0

	def __str__(self):
		return "Car %d: Position -> %s Capacity -> %s Avaible Seats -> %s" % (self.indx, self.position, self.capacity, str(self.capacity-self.load))

def initialize():
	return {i: Car(i, carPos[i-1], 2) for i in xrange(1, len(carPos)+1)}

def checkTimeWindow(req, cost):
	eStart = req.eStart
	eEnd = req.eEnd

	return ( ( (eStart+cost) == eEnd) )

def objFunction(string):

	assigns = [(i+1, string[i]) for i in xrange(len(string))]
	cars = initialize()
	#each car is separated by the requirements
	splitCars = {key: [x[0] for x in assigns if str(key) == x[1]] for key in xrange(1, variability+1)}
	#check the cars already in picked up
	inCar = {key:[] for key in xrange(1,variability+1)}

	score = 0

	for c in splitCars:
		flag = True
		print("Car %s" % c)
		#currentTime = requests[splitCars[c][0]].eStart
		currentTime = 24
		#if scores not change, it is not possible pick up and deleviry anyone
		while(flag):
			print("If repeating %s is a infinity loop" % string)
			flag = False

			#Cluster the pick-ups possibilities O(nCars * nReq)		
			for i in xrange(len(splitCars[c])):
				r = requests[splitCars[c][i]]
				if( ( cars[c].position == r.origin ) and
					( (cars[c].load + r.load) <= cars[c].capacity ) and
					( r.eStart <= currentTime ) ):

					inCar[c].append(r)
					cars[c].load = cars[c].load + r.load
					#print("Request %s is in car" % r)
					splitCars[c].pop(i)
					i = 0

			#check if it is possible deleviry requests already in the car
			for i in inCar[c]:
				if( (checkTimeWindow(i, graph[i.origin][i.destination])) ):
					print("Delivering %s" % i)
					score = score + 1
					flag = True
					cars[c].load = cars[c].load - i.load
					cars[c].position = i.destination
					inCar[c].remove(i)
					currentTime = currentTime + graph[i.origin][i.destination] 

	return score

def wrongAssigment(string):
	cars = initialize()
	wrong = []
	k = 0
	for r in string:
		req = requests.values()[k]
		if(cars[int(r)].position == req.origin and
			checkTimeWindow(req, graph[req.origin][req.destination]) ):
			cars[int(r)].position = req.destination
		else:
			wrong.append(k+1)
		k = k + 1

	return wrong
#Start variables
'''carPos = "AABCCDD"
#graph costs
graph = {'A' : {'B':   1, 'C':   1, 'D':   1},
		 'B' : {'A':   1, 'C': 2.5, 'D':   2},
		 'C' : {'A':   1, 'B': 2.5, 'D': 1.5},
		 'D' : {'A':   1, 'B':   2, 'C': 1.5}}
#requests
requests = {1:  Request( 1, 'A', 'B',    8,   10, 1), 
			2:  Request( 2, 'C', 'A',    8,   11, 1), 
			3:  Request( 3, 'B', 'A',    9,   10, 1), 
			4:  Request( 4, 'D', 'C',  9.5,   13, 1),
			5:  Request( 5, 'D', 'A',  9.5, 10.5, 1),
			6:  Request( 6, 'A', 'B', 10.5,   16, 1),
			7:  Request( 7, 'A', 'C',   11,   13, 1), 
			8:  Request( 8, 'D', 'A',   11,   16, 1),
			9:  Request( 9, 'A', 'D', 11.5, 12.5, 1),
			10: Request(10, 'B', 'C',   12, 14.5, 1),
			11: Request(11, 'D', 'B',   12,   15, 1),
			12: Request(12, 'B', 'D',   12, 15.5, 1),
			13: Request(13, 'C', 'D', 12.5,   14, 1),
			14: Request(14, 'C', 'A',   13,   15, 1),
			15: Request(15, 'B', 'A',   13,   15, 1),
			16: Request(16, 'D', 'C',   15,   17, 1),
			17: Request(17, 'A', 'D',   16, 17.5, 1),
			18: Request(18, 'C', 'B',   16,   19, 1),
			19: Request(19, 'C', 'A',   19, 20.5, 1),
			20: Request(20, 'A', 'B',   20,   22, 1)}

nReq = 20
population = 15
breeds = 50
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
	print("%d in position %s" % (cars[c].indx, cars[c].position))

print("\n>>>> NOT ACCEPTED REQUISITIONS <<<<\n")
for w in wrongs:
	print("Requisition %d was not possible" % w)
print("\nTotal of accepted requisitions: %d/%d" % ((len(best)-len(wrongs)), len(best)))
'''

nReq = 7
population = 6
breeds = 10
variability = 3
mutation = 0.3
copyFraction = 0.6

carPos = 'ABC'

graph = {'A' : {'B':   1, 'C':   2, 'D':   2},
		 'B' : {'A':   1, 'C':   1, 'D':   3},
		 'C' : {'A':   2, 'B':   1, 'D':   2},
		 'D' : {'A':   2, 'B':   3, 'C':   2}}
#requests
requests = {1:  Request( 1, 'A', 'B',    8,   11, 1), 
			2:  Request( 2, 'A', 'C',    8,   10, 1), 
			3:  Request( 3, 'C', 'D',    9,   12, 1), 
			4:  Request( 4, 'B', 'D',   11,   14, 1),
			5:  Request( 5, 'B', 'A',   11,   12, 1),
			6:  Request( 6, 'D', 'A',   15,   17, 1),
			7:  Request( 7, 'C', 'B',   16,   17, 1)}

#objFunction("1122133")
test = GA(nReq, population, breeds, variability, mutation, copyFraction, objFunction)
best = test.run()

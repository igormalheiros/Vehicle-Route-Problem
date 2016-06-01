from GA import GA


class Request:
	def __init__(self, indx, origin, destination):
		self.indx = indx
		self.origin = origin
		self.destination = destination

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

def objFunction(string):
	cars = initialize()

	k = 0
	score = 1

	for r in string:
		carId = int(r)-1
		if(cars[carId].position == requests[k].origin):
			score = score + 1
			cars[carId].position = requests[k].destination
		k = k+1

	return score


carPos = "AABCD"
requests = [Request(1, 'A', 'B'), Request(2, 'A', 'D'), Request(3, 'B', 'D'), Request(4, 'C', 'A'), Request(5, 'C', 'D'), Request(6, 'D', 'B')]

#print(objFunction("112235"))
#for c in cars:
#	print (c)
#print(objFunction("214435"))
#print(objFunction("453211"))
#print(objFunction("352451"))
test = GA(6, 10, 300, 5, 0.2, 0.5, objFunction)
print(test.run())

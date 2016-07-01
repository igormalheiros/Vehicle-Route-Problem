class SimpleRequest:

	def __init__(self, indx, startLocation, endLocation, eStart, eEnd, passengers):
		self.indx = indx
		self.startLocation = startLocation
		self.endLocation = endLocation
		self.eStart = eStart
		self.eEnd = eEnd
		self.passengers = passengers
		self.car = None

	def __str__(self):
		return "Request %d: %s to %s [%f] [%f] with %s passengers" % (self.indx, self.startLocation, self.endLocation, self.eStart, self.eEnd, self.passengers)	

class Request:

	def __init__(self, indx, startLocation, endLocation, eStart, lStart, eEnd, lEnd):
		self.indx = indx
		self.startLocation = startLocation
		self.endLocation = endLocation
		self.eStart = eStart
		self.lStart = lStart
		self.eEnd = eEnd
		self.lEnd = lEnd
		self.car = None

	def __str__(self):
		return "Request %d: %s to %s [%f,%f] [%f, %f]" % (self.indx, self.startLocation, self.endLocation, self.eStart, self.lStart, self.eEnd, self.lEnd)

class Car:

	def __init__(self, indx, position, capacity):
		self.indx = indx
		self.position = position
		self.capacity = capacity
		self.availableSeats = capacity

	def __str__(self):
		return "Car %d: Position -> %s Capacity -> %s Avaible Seats -> %s" % (self.indx, self.position, self.capacity, self.availableSeats)
class Request:

	def __init__(self, indx, origin, destination, eStart, lStart, eEnd, lEnd):
		self.indx = indx
		self.origin = origin
		self.destination = destination
		self.eStart = eStart
		self.lStart = lStart
		self.eEnd = eEnd
		self.lEnd = lEnd
		self.car = None

	def __str__(self):
		return "Request %d: %s to %s [%f,%f] [%f, %f]" % (self.indx, self.origin, self.destination, self.eStart, self.lStart, self.eEnd, self.lEnd)

class Car:

	def __init__(self, indx, position, capacity):
		self.indx = indx
		self.position = position
		self.capacity = capacity
		self.availableSeats = capacity

	def __str__(self):
		return "Car %d: Position -> %s Capacity -> %s Avaible Seats -> %s" % (self.indx, self.position, self.capacity, self.availableSeats)
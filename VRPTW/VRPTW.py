class Request:

	def __init__(self, indx, startLocation, endLocation, eStart, lStart, eEnd, lEnd, extraTime, passengers):
		self.indx = indx
		self.startLocation = startLocation
		self.endLocation = endLocation
		self.eStart = eStart
		self.lStart = lStart
		self.eEnd = eEnd
		self.lEnd = lEnd
		self.extraTime = extraTime
		self.passengers = passengers
		self.car = None

	def __str__(self):
		'''return "%s %s %d:%02d %d:%02d %d:%02d %d:%02d %d:%02d %d" % (self.startLocation, self.endLocation, 
														self.eStart/60, self.eStart%60, self.lStart/60, self.lStart%60,
														self.eEnd/60, self.eEnd%60, self.lEnd/60, self.lEnd%60, self.extraTime/60,
														self.extraTime%60, self.passengers)'''
		return "Request %d: %s to %s [%d:%02d,%d:%02d] [%d:%02d,%d:%02d] with %d:%02d extra time and %d passengers" % (self.indx, self.startLocation, self.endLocation, 
														self.eStart/60, self.eStart%60, self.lStart/60, self.lStart%60,
														self.eEnd/60, self.eEnd%60, self.lEnd/60, self.lEnd%60, self.extraTime/60,
														self.extraTime%60, self.passengers)

class Car:

	def __init__(self, indx, position, capacity):
		self.indx = indx
		self.position = position
		self.capacity = capacity
		self.availableSeats = capacity

	def __str__(self):
		return "Car %d: Position -> %s Capacity -> %s Avaible Seats -> %s" % (self.indx, self.position, self.capacity, self.availableSeats)
		#return "%s %s" % (self.position, self.capacity)
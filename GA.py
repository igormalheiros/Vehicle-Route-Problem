import random

#Class of individuals
class Individual:

	def __init__(self, gene):
		self.gene = gene
		self.score = 0

	def __str__(self):
		return "Individual: %s --- Score: %d" % (self.gene, self.score)

	def __radd__(self, other):
		return other + self.score

	def setScore(self, objFunction):
		self.score = objFunction(self.gene)

#Class of Genetic Algorithm
class GA:
	#
	def __init__(self, geneSize, populationSize, variability, mutation, fraction, objFunction):
		self.geneSize = geneSize
		self.populationSize = populationSize
		self.variability = variability
		self.mutation = mutation
		self.fraction = fraction
		self.objFunction = objFunction
		self.totalScore = 0

	def generateIndividual(self):
		gene = ""
		for i in xrange(self.geneSize):
			gene += str(random.randint(1, self.variability))
		return Individual(gene)

	def initializePopulation(self):
		return [self.generateIndividual() for x in xrange(self.populationSize)]

	def computeFitness(self, population):
		for i in population:
			i.setScore(self.objFunction)
		return population

	def roulleteSelection(self, population):
		totalScore = sum(population)
		r = random.random()
		total = 0.0
		for i in population:
			total += (i.score/float(totalScore))
			if(r < total):
				return i

	def copy(self, population):
		nCopy = int((1-self.fraction) * self.populationSize)
		copyPop = []
		for i in xrange(nCopy):
			indiv = self.roulleteSelection(population)
			copyPop.append(indiv)
			population.remove(indiv)

		return copyPop

#Test section

#Objective Function definition
def objFunction(string):
	return sum(int(x) for x in string)

test = GA(20, 4, 4, 0, 0.3, objFunction)
pop = test.initializePopulation()
pop = test.computeFitness(pop)
print("------Start Generation------")
for p in pop:
	print(p)
print("-------Copy---------")
for p in test.copy(pop):
	print(p)
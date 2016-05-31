import random

#Class of individuals
class Individual:

	def __init__(self, gene):
		self.gene = gene
		self.score = 0

	def __str__(self):
		return "Individual: %s --- Score: %d" % (self.gene, self.score)

	def __getitem__(self, indx):
		return self.gene[indx]

	def __radd__(self, other):
		return other + self.score

	def __len__(self):
		return len(self.gene)

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
		nCopy = int((1.0-self.fraction) * self.populationSize)
		copyPopulation = [p for p in population]
		nextGeneration = []

		for i in xrange(nCopy):
			indiv = self.roulleteSelection(copyPopulation)
			nextGeneration.append(indiv)
			copyPopulation.remove(indiv)

		return nextGeneration

	def onePoint(self, indiv1, indiv2):
		return Individual(indiv1[:(len(indiv1)/2)] + indiv2[(len(indiv2)/2):])

	def crossover(self, population, nextGeneration):

		nChildrens = int(self.fraction * self.populationSize)

		for i in xrange(nChildrens):
			copyPopulation = [p for p in population]

			parent1 = self.roulleteSelection(copyPopulation)
			copyPopulation.remove(parent1)
			parent2 = self.roulleteSelection(copyPopulation)

			nextGeneration.append(self.onePoint(parent1, parent2))

		return nextGeneration

#Test section

#Objective Function definition
def objFunction(string):
	return sum(int(x) for x in string)

test = GA(20, 10, 4, 0, 0.5, objFunction)
pop = test.initializePopulation()
pop = test.computeFitness(pop)

print("------Start Generation------")
for p in pop:
	print(p)

print("-------Copy---------")
copy = test.copy(pop)
for p in copy:
	print(p)

print("-------Crossover---------")
cross = test.crossover(pop, copy)
for p in cross:
	print(p)
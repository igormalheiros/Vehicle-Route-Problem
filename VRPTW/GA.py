import random
from operator import attrgetter

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
	
	def __init__(self, geneSize, populationSize, breed,variability, mutation, fraction, objFunction):
		self.geneSize = geneSize
		self.populationSize = populationSize
		self.breed = breed
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

	def evaluate(self, population):
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
		nextBreed = []

		for i in xrange(nCopy):
			indiv = self.roulleteSelection(copyPopulation)
			nextBreed.append(indiv)
			copyPopulation.remove(indiv)

		return nextBreed

	def onePoint(self, indiv1, indiv2):
		return Individual(indiv1[:(len(indiv1)/2)] + indiv2[(len(indiv2)/2):])

	def crossover(self, population, nextBreed):
		nChildrens = int(self.fraction * self.populationSize)

		for i in xrange(nChildrens):
			parent1 = self.roulleteSelection(population)
			parent2 = self.roulleteSelection(population)

			while(parent2 == parent1):
				parent2 = self.roulleteSelection(population)

			nextBreed.append(self.onePoint(parent1, parent2))

		return nextBreed

	def mutate(self, nextBreed):
		r = int(self.mutation * self.populationSize)
		
		for i in xrange(r):
			chosenIndividual = random.choice(nextBreed)
			chosenChromossome = random.randint(0, self.geneSize-1)
			chosenValue = random.randint(1, self.variability)
			nextBreed.remove(chosenIndividual)
			aux = list(chosenIndividual.gene)
			aux[chosenChromossome] = str(chosenValue)
			nextBreed.append(Individual("".join(aux)))

		return nextBreed

	def run(self):
		k = 0
		p = self.initializePopulation()
		p = self.evaluate(p)

		print("------Start Breed------")
		for i in p:
			print(i)

		print("------Best on First Breed------")
		print(max(p, key=attrgetter('score')))

		while(k < self.breed):
			k = k + 1
			c = self.copy(p)
			p = self.crossover(p, c)
			p = self.mutate(p)
			p = self.evaluate(p)

		print("------Last Breed------")
		for i in p:
			print(i)

		print("FINAL RESULT")
		best = max(p, key=attrgetter('score'))
		print(best)
		return best

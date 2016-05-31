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
	#
	def __init__(self, geneSize, populationSize, generation,variability, mutation, fraction, objFunction):
		self.geneSize = geneSize
		self.populationSize = populationSize
		self.generation = generation
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

	def mutate(self, nextGeneration):
		r = int(self.mutation * self.populationSize)
		for i in xrange(r):
			chosenIndividual = random.choice(nextGeneration)
			chosenChromossome = random.randint(0, self.geneSize-1)
			chosenValue = random.randint(1, self.variability)
			nextGeneration.remove(chosenIndividual)
			aux = list(chosenIndividual.gene)
			aux[chosenChromossome] = str(chosenValue)
			nextGeneration.append(Individual("".join(aux)))
		return nextGeneration

	def run(self):
		k = 0
		p = self.initializePopulation()
		p = self.evaluate(p)

		print("------Start Generation------")
		for i in p:
			print(i)

		while(max(p, key=attrgetter('score')) < (self.variability*self.geneSize) and k < self.generation):

			k = k + 1
			c = test.copy(p)
			p = test.crossover(p, c)
			p = test.mutate(p)
			p = self.evaluate(p)

			#print("------New Generation------")
			#for i in p:
			#	print(i)

		print("------Last Generation------")
		for i in p:
			print(i)
			
		print("FINAL RESULT")
		return max(p, key=attrgetter('score'))

#Test section

#Objective Function definition
def objFunction(string):
	return sum(int(x) for x in string)

test = GA(20, 100, 3000, 4, 0.2, 0.5, objFunction)
print(test.run())

from random import randint

#Class of individuals
class Individual:

	def __init__(self, gene):
		self.gene = gene
		self.score = 0

	def __str__(self):
		return "Individual: %s --- Score: %d" % (self.gene, self.score)

	def setScore(self, objFucntion):
		self.score = objFucntion
		
#Class of Genetic Algorithm
class GA:
	#
	def __init__(self, geneSize, populationSize, variability, mutation):
		self.geneSize = geneSize
		self.populationSize = populationSize
		self.variability = variability
		self.mutation = mutation 

	def generateIndividual(self):
		gene = ""
		for i in xrange(self.geneSize):
			gene += str(randint(1, self.variability))
		return Individual(gene)

	def initializePopulation(self):
		return [generateIndividual(self.geneSize, self.variability) for x in xrange(self.populationSize)]

test = GA(20, 4, 4, 0)
print(test.generateIndividual())
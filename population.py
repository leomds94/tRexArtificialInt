from random import random
import numpy as np
from individual import Individual

class Population():
    
    def __init__(self, populationSize, chromosomeLength=0):
        
        self.fitness = -1
        self.individuals = []
        
        for i in range(populationSize):
            ind = Individual([])
            ind.initialize(chromosomeLength)
            self.individuals.append(ind)
            
    def fittest(self, index):
        self.individuals.sort(key=lambda ind: ind.fitness, reverse=True)
        return self.individuals[index]

    def addIndividual(self, chromosomes, index):
        new_chromosomes = []
        for c in chromosomes:
            new_chromosomes.append(c)
        self.individuals[index] = Individual(new_chromosomes)
        
    
    def shuffle(self):
        for i in reversed(range(self.size)):
            index = random() * len(self.size)
            individual = self.individuals[index]
            self.individuals[index] = self.individuals[i]
            self.individuals[i] = individual

    def size(self):
        return len(self.individuals)
    
    def __repr__(self):
        return "[{}] Population Fitenss: {}, Size: {}".format(
            self.__class__.__name__, 
            self.fitness, 
            self.size())
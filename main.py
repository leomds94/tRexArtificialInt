# -*- coding: utf-8 -*-
from threading import Thread
from genetic_algorithm import GeneticAlgorithm
import sys

import pykeyboard

ga = GeneticAlgorithm(10, 12, 0.001, 0.95, 2)

while(True):

    ga.evaluate_population()
    try:
        print(ga.population.fittest(0).chromosome)
    except:
        sys.exc_info()[0]

    print("Fitness:",ga.population.fitness)

    ga.population = ga.crossover_population()
    ga.population = ga.mutate_population()

print("Best solution: ", ga.population.fittest(0).chromosome)
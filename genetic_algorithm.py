# -*- coding: utf-8 -*-
from random import random
import numpy as np
import pykeyboard
from time import sleep

from scanner import Scanner
from mlp import Network

from time import sleep
from individual import Individual
from population import Population

class GeneticAlgorithm():

    def __init__(self, population_size, chromosome_length, mutation_rate, crossover_rate, elitism_count):
        self.population = self.init_population(population_size, chromosome_length)
        #trained1 = [-0.7804749316601893, 0.1513393337247957, -0.2768261313809339, 0.4701464868308525, 0.3439301467453155, 0.8967267012585185, -0.073053272613403, -0.8093484800832229, 0.11935976376011337, 0.3656041574367368, -0.25653148336315446, -0.46913389704113073]
        #self.population.addIndividual(trained1, 0)
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        self.mlp = Network()
        self.scanner = Scanner()
        self.k = pykeyboard.PyKeyboard()
        self.up_pressed = False
        self.down_pressed = False

        self.scanner.find_game()

        self.k.press_key(self.k.alt_key)
        self.k.tap_key(self.k.tab_key)
        self.k.release_key(self.k.alt_key)

    def init_population(self, population_size, chromosome_length):
        self.population = Population(population_size, chromosome_length)
        return self.population

    def press_key(self, key):
        if key == 'Up':
            self.up_pressed = True
            self.k.press_key(self.k.up_key)
        elif key == 'Down':
            self.down_pressed = True
            self.k.press_key(self.k.down_key) 

    def release_key(self, key):
        if key == 'Up':
            self.up_pressed = False
            self.k.release_key(self.k.up_key)
        elif key == 'Down':
            self.down_pressed = False
            self.k.release_key(self.k.down_key) 

    def calculate_individual_fitness(self, individual):
        self.scanner.reset()
        sleep(0.5)
        self.k.tap_key(self.k.space)

        if self.up_pressed:
            self.release_key('Up')
        elif self.down_pressed:
            self.release_key('Down')
            
        self.scanner.find_dino()
        sleep(0.5)
        last = 0.5

        while True:
            try:
                obs = self.scanner.find_next_obstacle(self.down_pressed)
                #print("dist: {}, length: {}, speed: {}").format(obs['distance'], obs['length'], obs['speed'])
                inputs = [obs['distance'] / 1000.0, obs['length'] / 100.0, obs['speed'] / 10.0]
                outputs = self.mlp.forward(np.array(inputs, dtype=float))

                if last > -0.25 and outputs[0] <= -0.25 and self.up_pressed:
                   self.release_key('Up')
                elif last < -0.45 and outputs[0] >= -0.45 and self.down_pressed:
                   self.release_key('Down')

                if outputs[0] > -0.25:
                    self.press_key('Up')
                elif outputs[0] < -0.45:
                    self.press_key('Down')
                last = outputs[0]

                print last
            except:
                sleep(0.5)
                break
        return self.scanner.get_fitness()

    def evaluate_population(self):
        population_fitness = 0
        for individual in self.population.individuals:
            individual_fitness = self.calculate_individual_fitness(individual)
            if(population_fitness < individual_fitness):
                population_fitness = individual_fitness
        self.population.fitness = population_fitness
    
    def crossover_population(self):
        new_population = Population(self.population.size())
        
        for individual_index in range(self.population.size()):
            parent1 = self.population.fittest(individual_index)
            
            if self.crossover_rate > random() and individual_index >= self.elitism_count:
                offspring = Individual([])
                offspring.initialize(parent1.chromosome_size())
                parent2 = self.select_parent()
                
                for gene_index in range(parent1.chromosome_size()):
                    if random() > 0.5:
                        offspring.chromosome[gene_index] = parent1.chromosome[gene_index]
                    else:
                        offspring.chromosome[gene_index] = parent2.chromosome[gene_index]  
                new_population.individuals[individual_index] = offspring
            else:
                new_population.individuals[individual_index] = parent1   
        return new_population
    
    def mutate_population(self):
        
        new_population = Population(self.population.size())
        
        for population_index in range(self.population.size()):
            individual = self.population.fittest(population_index)
        
            for gene_index in range(individual.chromosome_size()):

                if population_index >= self.elitism_count:

                    if self.mutation_rate > random():
                        individual.chromosome[gene_index] = random()
                        
            new_population.individuals[population_index] = individual
            
        return new_population
        
    
    def select_parent(self):
        individuals = self.population.individuals
        roulette_whell_position = random() * self.population.fitness
        
        spin_whell = 0
        for individual in individuals:
            spin_whell += individual.fitness
            if spin_whell >= roulette_whell_position:
                return individual
            
        return individuals[-1]

import numpy as np

class Individual():


    def __init__(self, chromosome):
        
        self.chromosome = chromosome
        self.fitness = 0.0
        
    def initialize(self, chromosome_length):
        self.chromosome = []
        #self.chromosome.append([0.5355107045415289, 0.4919988754299607, 0.7258417508196696, 0.8088697447225727, 0.13359664782715208, 0.2921003549698703, 0.22279321239650995, 0.09342575650485552, 0.781157483128532, 0.41348017608374743, 0.3011797358078929, 0.3203754458552095])
        for i in range(chromosome_length):
            self.chromosome.append(np.random.uniform(-1, 1))
                
    def chromosome_size(self):
        return len(self.chromosome)
        
    def __repr__(self):
        return "Fitness: {}, Chromosome: {}".format( 
            self.fitness, self.chromosome)
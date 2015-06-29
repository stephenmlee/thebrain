import copy
import random
from CommandBunker.ControlPanel import INITIAL_POPULATION_SIZE, WEIGHT_MUTATION_POWER, WEIGHT_MUTATION_TAIL_BOOST

__author__ = 'stephen'


class Population(object):
    def __init__(self, starting_genome):
        self.organisms = [starting_genome]
        for count in range(1, INITIAL_POPULATION_SIZE):
            clone = copy.deepcopy(starting_genome)
            clone["id"] = count
            tail_index = 0.8*len(clone["synapses"])
            for index, synapse in enumerate(clone["synapses"]):
                tail_boost = WEIGHT_MUTATION_TAIL_BOOST if index > tail_index else 1
                synapse["weight"] += self.rand_pos_neg() * random.random() * WEIGHT_MUTATION_POWER * tail_boost
            self.organisms.append(clone)

    def rand_pos_neg(self):
        return -1 if random.randint(0, 1) == 0 else 1

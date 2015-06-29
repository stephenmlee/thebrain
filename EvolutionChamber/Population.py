import copy
from CommandBunker.ControlPanel import INITIAL_POPULATION_SIZE

__author__ = 'stephen'

class Population(object):
    def __init__(self, starting_genome):
        organisms = []
        for count in range(1, INITIAL_POPULATION_SIZE):
            clone = copy.deepcopy(starting_genome)
            clone.id = count



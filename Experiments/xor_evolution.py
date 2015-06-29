import unittest

__author__ = 'stephen'


class RunExperiment(unittest.TestCase):
    def evolve_xor(self):
        starting_genome = self.read_genome('Experiments/CryogenicStorage/minimal_genome.json')
        population = Population(starting_genome)

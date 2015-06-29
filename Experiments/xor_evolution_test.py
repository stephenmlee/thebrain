import json
import unittest
from EvolutionChamber.Population import Population

__author__ = 'stephen'


class RunExperiment(unittest.TestCase):
    def test_evolve_xor(self):
        starting_genome = decode('Experiments/CryogenicStorage/minimal_genome.json')
        population = Population(starting_genome)
        self.assertEqual(len(population.organisms), 500)


def decode(genome_file):
    f = open(genome_file, 'r')
    genome = json.load(f)
    f.close()
    return genome

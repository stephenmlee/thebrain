import json
import unittest
from EvolutionChamber.Population import Population

__author__ = 'stephen'


class RunExperiment(unittest.TestCase):
    def test_create_initial_population(self):
        starting_genome = decode('Experiments/CryogenicStorage/minimal_genome.json')
        population = Population(starting_genome)
        self.assertEqual(len(population.organisms), 500)
        self.assertEqual(len(population.species), 1)


def decode(genome_file):
    f = open(genome_file, 'r')
    genome = json.load(f)
    f.close()
    return genome

import json
import unittest

from Cranium import NeuralNetwork


class RunExperiment(unittest.TestCase):
    def test_extract_genome(self):

        expected_genome = self.read_genome('Experiments/CryogenicStorage/xor_genome.json')
        brain = NeuralNetwork.expressed_from(expected_genome)
        genome = brain.decode_genome()
        self.maxDiff = None
        self.assertEqual(genome, expected_genome)

    def read_genome(self, genome_file):
        f = open(genome_file, 'r')
        expected_genome = json.load(f)
        f.close()
        return expected_genome

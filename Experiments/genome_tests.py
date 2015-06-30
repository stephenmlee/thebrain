import json
import unittest

from Cranium import NeuralNetwork
from EvolutionChamber.GeneSplicer import GeneSplicer


class RunExperiment(unittest.TestCase):
    def test_extract_genome(self):
        expected_genome = self.read_genome('Experiments/CryogenicStorage/xor_genome.json')
        brain = NeuralNetwork.expressed_from(expected_genome)
        genome = brain.decode_genome()
        self.maxDiff = None
        self.assertEqual(genome, expected_genome)

    def test_compatibility_of_identical_genomes(self):
        genome = self.read_genome('Experiments/CryogenicStorage/xor_genome.json')
        splicer = GeneSplicer()
        self.assertEqual(splicer.compatibility_scan(genome, genome), 0)

    def test_compatibility_of_different_genomes(self):
        genome1 = self.read_genome('Experiments/CryogenicStorage/xor_genome.json')
        genome2 = self.read_genome('Experiments/CryogenicStorage/xor_genome.json')

        del genome1["synapses"][2]
        del genome2["synapses"][6:9]
        genome2["synapses"][3]["weight"] = 1.5

        splicer = GeneSplicer()
        self.assertEqual(splicer.compatibility_scan(genome1, genome2), 0.2664)

    def read_genome(self, genome_file):
        f = open(genome_file, 'r')
        expected_genome = json.load(f)
        f.close()
        return expected_genome

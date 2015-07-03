import json
import unittest

from Cranium import NeuralNetwork


class RunExperiment(unittest.TestCase ):
    def test_output_is_zero_when_both_inputs_are_zero(self):
        genome = decode('CryogenicStorage/xor_genome.json')
        brain = NeuralNetwork.expressed_from(genome)
        brain.stimulate([("S1", 0),
                         ("S2", 0)])
        brain.electrify()
        self.assertLess(brain.outputs()["O1"].activation(), 0.1)

    def test_output_is_one_when_s1_is_one(self):
        genome = decode('CryogenicStorage/xor_genome.json')
        brain = NeuralNetwork.expressed_from(genome)
        brain.stimulate([("S1", 1),
                         ("S2", 0)])
        brain.electrify()
        self.assertGreater(brain.outputs()["O1"].activation(), 0.9)

    def test_output_is_one_when_s2_is_one(self):
        genome = decode('CryogenicStorage/xor_genome.json')
        brain = NeuralNetwork.expressed_from(genome)
        brain.stimulate([("S1", 1),
                         ("S2", 0)])
        brain.electrify()
        self.assertGreater(brain.outputs()["O1"].activation(), 0.1)

    def test_output_is_zero_when_both_inputs_are_one(self):
        genome = decode('CryogenicStorage/xor_genome.json')
        brain = NeuralNetwork.expressed_from(genome)
        brain.stimulate([("S1", 1),
                         ("S2", 1)])
        brain.electrify()
        self.assertLess(brain.outputs()["O1"].activation(), 0.9)

def decode(genome_file):
    f = open(genome_file, 'r')
    genome = json.load(f)
    f.close()
    return genome




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
        activation = brain.outputs()["O1"].activation()
        self.assertLess(activation, 0.001)
        print "0, 0: %.8f" % activation

    def test_output_is_one_when_s1_is_one(self):
        genome = decode('CryogenicStorage/xor_genome.json')
        brain = NeuralNetwork.expressed_from(genome)
        brain.stimulate([("S1", 1),
                         ("S2", 0)])
        brain.electrify()
        activation = brain.outputs()["O1"].activation()
        self.assertGreater(activation, 0.999)
        print "0, 1: %.8f" % activation

    def test_output_is_one_when_s2_is_one(self):
        genome = decode('CryogenicStorage/xor_genome.json')
        brain = NeuralNetwork.expressed_from(genome)
        brain.stimulate([("S1", 1),
                         ("S2", 0)])
        brain.electrify()
        activation = brain.outputs()["O1"].activation()
        self.assertGreater(activation, 0.001)
        print "1, 0: %.8f" % activation

    def test_output_is_zero_when_both_inputs_are_one(self):
        genome = decode('CryogenicStorage/xor_genome.json')
        brain = NeuralNetwork.expressed_from(genome)
        brain.stimulate([("S1", 1),
                         ("S2", 1)])
        brain.electrify()
        activation = brain.outputs()["O1"].activation()
        self.assertLess(activation, 0.999)
        print "1, 1: %.8f" % activation

def decode(genome_file):
    f = open(genome_file, 'r')
    genome = json.load(f)
    f.close()
    return genome




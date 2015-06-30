import json
from Cranium import NeuralNetwork
from Cranium.NeuralNetwork import UnstableNetworkError
from EvolutionChamber.Population import Population

__author__ = 'stephen'


def decode(genome_file):
    f = open(genome_file, 'r')
    g = json.load(f)
    f.close()
    return g


if __name__ == "__main__":
    starting_genome = decode('Experiments/CryogenicStorage/minimal_genome.json')
    population = Population(starting_genome)

    for genome in population.organisms:
        brain = NeuralNetwork.expressed_from(genome)

        inputs = [[("S1", 0), ("S2", 0)], [("S1", 0), ("S2", 1)], [("S1", 1), ("S2", 0)], [("S1", 1), ("S2", 1)]]

        desired_outputs = [0, 1, 1, 0]
        actual_outputs = []

        try:
            for sensory_input in inputs:
                brain.stimulate(sensory_input)
                brain.electrify()
                actual_outputs.append(brain.outputs()["O1"].activation())
            error = actual_outputs[0] + (1 - actual_outputs[1]) + (1 - actual_outputs[2]) + actual_outputs[3]
            genome["fitness"] = 4 - error

        except UnstableNetworkError:
            print genome["id"] + " is UNSTABLE!!!"

    organism = population.max_fitness_species().max_fitness_organism()
    print "Max Fitness: Organism " + str(organism["id"]) + " with " + str(organism["fitness"])
    print json.dumps(organism, indent=2)




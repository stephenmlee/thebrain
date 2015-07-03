import json
import thread
import time
import math
from CommandBunker.ControlPanel import AGE_DROPOFF_THRESHOLD
from Cranium import NeuralNetwork
from Cranium.NeuralNetwork import UnstableNetworkError
from EvolutionChamber.Population import Population

__author__ = 'stephen'


def decode(genome_file):
    f = open(genome_file, 'r')
    g = json.load(f)
    f.close()
    return g


def generate():
    n = 0
    while True:
        n += 1
        yield "." if n % 2 == 0 else "+"


if __name__ == "__main__":
    starting_genome = decode('Experiments/CryogenicStorage/minimal_genome.json')
    population = Population(starting_genome)

    target_fitness = math.pow(3.9,2)
    best_fitness = 0
    generation = 1
    last_improvement = 0

    while best_fitness < target_fitness:

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
                genome["fitness"] = math.pow(4 - error, 2)

            except UnstableNetworkError:
                genome["fitness"] = 0
                #print "%s is UNSTABLE!!!" % genome["id"]

        organism = population.max_fitness_species().max_fitness_organism()

        if organism["fitness"] > best_fitness:
            best_fitness = organism["fitness"]
            last_improvement = 0
        else:
            last_improvement += 1
            if last_improvement > AGE_DROPOFF_THRESHOLD * 100:
                print json.dumps(organism, indent=2)
                time.sleep(1)
                raise Exception("STAGNANT POPULATION")

        zoo = []
        for species in population.species:
            zoo.extend(species.id for x in range(0, len(species.member_organisms)))

        population.EPOCH()
        generation += 1

        zoo = []
        for species in population.species:
            zoo.extend(species.id for x in range(0, len(species.member_organisms)))

        last_species_id = 0

        population_map = ""
        genorator = generate()
        species_character = genorator.next()
        for sample in range(0, 100):
            sampled_species_id = zoo[int(sample*(len(zoo)/100))]
            if sampled_species_id != last_species_id:
                last_species_id = sampled_species_id
                species_character = genorator.next()
            population_map += species_character
        print population_map + " : EPOCH %s -- Population: %s, Species: %s, Max Fitness: %s (%s)," % (
        generation, len(population.organisms), len(population.species), organism["fitness"], organism["id"])

    print json.dumps(population.max_fitness_species().max_fitness_organism())

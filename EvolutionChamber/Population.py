import copy
import random
import math
from CommandBunker.ControlPanel import INITIAL_POPULATION_SIZE, WEIGHT_MUTATION_POWER, WEIGHT_MUTATION_TAIL_BOOST, \
    COMPATIBILITY_THRESHOLD
from EvolutionChamber.GeneSplicer import GeneSplicer
from EvolutionChamber.Species import Species

__author__ = 'stephen'


class Population(object):
    def __init__(self, starting_genome):
        self.organisms = [starting_genome]
        self.species = []

        for count in range(1, INITIAL_POPULATION_SIZE):
            clone = copy.deepcopy(starting_genome)
            clone["id"] = count
            tail_index = 0.8 * len(clone["synapses"])
            for index, synapse in enumerate(clone["synapses"]):
                tail_boost = WEIGHT_MUTATION_TAIL_BOOST if index > tail_index else 1
                synapse["weight"] += self.rand_pos_neg() * random.random() * WEIGHT_MUTATION_POWER * tail_boost
            self.organisms.append(clone)

        self.speciate()

    def rand_pos_neg(self):
        return -1 if random.randint(0, 1) == 0 else 1

    def speciate(self):
        splicer = GeneSplicer()
        for organism in self.organisms:
            compatible = False
            count = 0
            while not compatible and count < len(self.species):
                species = self.species[count]
                if splicer.compatibility_scan(species.representative, organism) < COMPATIBILITY_THRESHOLD:
                    compatible = True
                    species.assimilate(organism)
                count += 1

            if not compatible:
                self.species.append(Species(organism))

    def max_fitness_species(self):
        return max(self.species, key=lambda s: s.max_fitness_organism())

    def EPOCH(self):
        for species in self.species:
            species.adjust_fitness()

        total_adjusted_fitness = 0
        for organism in self.organisms:
            total_adjusted_fitness += organism["adjusted_fitness"]
        average_adjusted_fitness = total_adjusted_fitness / len(self.organisms)

        for species in self.species:
            species.calc_number_of_offspring(average_adjusted_fitness)
        missing_children = len(self.organisms) - math.floor(sum(s.expected_children for s in self.species))
        self.max_fitness_species().expected_children += missing_children

        self.organisms = []
        for species in self.species:
            species.smite()
            self.organisms.extend(species.member_organisms)





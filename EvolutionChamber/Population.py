import copy
import random
import math
from CommandBunker import ControlPanel
from CommandBunker.ControlPanel import INITIAL_POPULATION_SIZE, WEIGHT_MUTATION_POWER, WEIGHT_MUTATION_TAIL_BOOST, \
    COMPATIBILITY_THRESHOLD, AGE_DROPOFF_THRESHOLD, next_organism_number
from EvolutionChamber.GeneSplicer import GeneSplicer
from EvolutionChamber.Species import Species

__author__ = 'stephen'


class Population(object):
    def __init__(self, starting_genome):
        self.organisms = [starting_genome]
        self.species = []
        ControlPanel.organism_number = 1

        for count in range(1, INITIAL_POPULATION_SIZE):
            clone = copy.deepcopy(starting_genome)
            clone["id"] = next_organism_number()
            GeneSplicer().mutate(clone)
            self.organisms.append(clone)

        self.speciate()

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
        return max(self.species, key=lambda s: s.max_fitness_organism()["fitness"])

    def EPOCH(self, generation):
        for species in self.species:
            species.adjust_fitness()

        total_adjusted_fitness = 0
        for organism in self.organisms:
            total_adjusted_fitness += organism["adjusted_fitness"]
        average_adjusted_fitness = total_adjusted_fitness / len(self.organisms)

        for species in self.species:
            species.calc_number_of_offspring(average_adjusted_fitness)

        for species in self.species:
            species.smite()

        if len(self.species) > 1:
            self.species = filter(lambda s: (len(
                s.member_organisms) > 0 and s.last_improvement < AGE_DROPOFF_THRESHOLD) or s.haschamp(),
                                  self.species)
            if len(self.species) == 0:
                raise Exception("NO MORE SPECIES LEFT... THEY ALL DIED!")

        missing_children = INITIAL_POPULATION_SIZE - sum(
            int(s.expected_children) + len(s.member_organisms) for s in self.species)
        self.max_fitness_species().expected_children += missing_children

        mutant_children = []
        for species in self.species:
            mutant_children.extend(species.breed(generation))

        self.invaded_by(mutant_children)

        self.organisms = []
        for species in self.species:
            self.organisms.extend(species.member_organisms)
            species.age += 1

    def invaded_by(self, mutants):
        lonesome_george = True
        for mutant in mutants:
            for species in self.species:
                splicer = GeneSplicer()
                if lonesome_george and splicer.compatibility_scan(species.representative,
                                                                  mutant) < COMPATIBILITY_THRESHOLD:
                    species.member_organisms.append(mutant)
                    lonesome_george = False
            if lonesome_george:
                self.species.append(Species(mutant))

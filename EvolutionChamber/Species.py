import math
from CommandBunker.ControlPanel import AGE_DROPOFF_THRESHOLD, YOUNG_BOOST, SURVIVAL_RATE

__author__ = 'stephen'


class Species(object):
    def __init__(self, representative):
        self.representative = representative
        self.member_organisms = [representative]
        self.last_improvement = 0
        self.max_fitness = 0
        self.age = 0
        self.expected_children = 0

    def assimilate(self, organism):
        self.member_organisms.append(organism)

    def max_fitness_organism(self):
        return max(self.member_organisms, key=lambda o: o["fitness"])

    def adjust_fitness(self):
        if self.max_fitness_organism()["fitness"] > self.max_fitness:
            self.max_fitness = self.max_fitness_organism()["fitness"]
            self.last_improvement = 0
        else:
            self.last_improvement += 1

        for organism in self.member_organisms:
            if self.last_improvement > AGE_DROPOFF_THRESHOLD:
                organism["adjusted_fitness"] = 0

            if self.age <= 10:
                organism["adjusted_fitness"] = organism["fitness"] * YOUNG_BOOST

            organism["adjusted_fitness"] /= len(self.member_organisms)

        self.member_organisms = sorted(self.member_organisms, key=lambda f: f["adjusted_fitness"])
        survivors = int(math.floor(SURVIVAL_RATE * len(self.member_organisms) + 1))
        for doomed in self.member_organisms[survivors:]:
            doomed["marked_for_death"] = "Yes"

    def calc_number_of_offspring(self, average_fitness):
        self.expected_children = 0
        for organism in self.member_organisms:
            self.expected_children += organism["adjusted_fitness"] / average_fitness

    def smite(self):
        self.member_organisms = filter(lambda o: o.get("marked_for_death", "No") == "No", self.member_organisms)

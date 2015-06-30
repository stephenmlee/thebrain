__author__ = 'stephen'


class Species(object):
    def __init__(self, representative):
        self.representative = representative
        self.member_organisms = [representative]

    def assimilate(self, organism):
        self.member_organisms.append(organism)

    def max_fitness_organism(self):
        return max(self.member_organisms, key=lambda o: o["fitness"])

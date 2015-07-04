__author__ = 'stephen'

innovation_number = 7
organism_number = 1
species_id = 0

INITIAL_POPULATION_SIZE = 150
WEIGHT_MUTATION_POWER = 2
WEIGHT_MUTATION_TAIL_BOOST = 1.2
RESET_WEIGHT_PROBABILITY = 0.05
DISJOINT_COEFF = 1
EXCESS_COEFF = 1
MUTATION_DIFF_COEFF = 0.4
COMPATIBILITY_THRESHOLD = 3
AGE_DROPOFF_THRESHOLD = 50
YOUNG_BOOST = 1
SURVIVAL_RATE = 0.2
MATE_PROBABILITY = 0.75
MUTATE_LINKS_PROBABILITY = 0.9
DISABLE_GENE_PROBABILITY = 0.01
REENABLE_GENE_PROBABILITY = 0.01
ADD_NODE_PROBABILITY = 0.3
ADD_LINK_PROBABILITY = 0.08

def next_innovation_number():
    global innovation_number
    innovation_number += 1
    return innovation_number

def next_organism_number():
    global organism_number
    organism_number += 1
    return organism_number


def next_species_id():
    global species_id
    species_id += 1
    return species_id
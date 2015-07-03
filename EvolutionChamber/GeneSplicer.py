import random
from CommandBunker import ControlPanel
from CommandBunker.ControlPanel import DISJOINT_COEFF, EXCESS_COEFF, MUTATION_DIFF_COEFF, MUTATE_LINKS_PROBABILITY, \
    DISABLE_GENE_PROBABILITY, REENABLE_GENE_PROBABILITY, ADD_NODE_PROBABILITY, ADD_LINK_PROBABILITY, \
    WEIGHT_MUTATION_TAIL_BOOST, WEIGHT_MUTATION_POWER, RESET_WEIGHT_PROBABILITY
from Cranium.Neuron import BIAS, HIDDEN
from EvolutionChamber import Randomiser

__author__ = 'stephen'


class GeneSplicer(object):
    def __init__(self):
        pass

    def compatibility_scan(self, genome1, genome2):
        genes1 = genome1["synapses"]
        genes2 = genome2["synapses"]
        g1 = 0
        g2 = 0
        num_excess = 0
        num_disjoint = 0
        num_matching = 0
        mutation_difference = 0
        max_genome_size = max(len(genes1), len(genes2))

        while g1 < len(genes1) and g2 < len(genes2):
            if g1 >= len(genes2):
                num_excess += 1
                g1 += 1
            elif g2 >= len(genes1):
                num_excess += 1
                g2 += 1
            else:
                innov1 = genes1[g1]["innovation_number"]
                innov2 = genes2[g2]["innovation_number"]
                if innov1 == innov2:
                    num_matching += 1
                    mutation_difference += abs(genes1[g1]["weight"] - genes2[g2]["weight"])
                    g1 += 1
                    g2 += 1
                elif innov1 < innov2:
                    num_disjoint += 1
                    g1 += 1
                else:
                    num_disjoint += 1
                    g2 += 1

        return (DISJOINT_COEFF * (num_disjoint / max_genome_size) +
                EXCESS_COEFF * (num_excess / max_genome_size)
                + MUTATION_DIFF_COEFF * (mutation_difference / num_matching))

    def mate(self, mum, dad):
        return dad

    def mutate(self, junior):
        pass

        if random.random() < DISABLE_GENE_PROBABILITY:
            synapse_genes = junior["synapses"]
            random_gene = synapse_genes[random.randint(0, len(synapse_genes) - 1)]
            random_gene["disabled"] = "true"

        if random.random() < REENABLE_GENE_PROBABILITY:
            pass

        if random.random() < ADD_NODE_PROBABILITY:
            synapse_genes = junior["synapses"]
            random_gene = synapse_genes[random.randint(0, len(synapse_genes) - 1)]

            old_dendrite = random_gene["dendrite"]
            old_axon = random_gene["axon"]

            if old_axon[:1] in ["S", "H"]:
                random_gene["disabled"] = "true"
                new_neuron = self.new_neuron()
                junior["neurons"].append(new_neuron)
                junior["synapses"].append(self.new_synapse(old_axon, new_neuron["label"], 1))
                junior["synapses"].append(self.new_synapse(new_neuron["label"], old_dendrite, random_gene["weight"]))

        if random.random() < ADD_LINK_PROBABILITY:
            neurons = junior["neurons"]
            random_neuron_1 = neurons[random.randint(0, len(neurons) - 1)]
            random_neuron_2 = neurons[random.randint(0, len(neurons) - 1)]
            if random_neuron_1["type"] not in ["Output"] and random_neuron_2["type"] not in ["Sensor", "Bias"]:
                junior["synapses"].append(self.new_synapse(random_neuron_1["label"], random_neuron_2["label"], 1))

        KRYPTONITE = 1
        if random.random() < 0.01:
            KRYPTONITE = 5

        if random.random() < MUTATE_LINKS_PROBABILITY:
            tail_index = 0.8 * len(junior["synapses"])
            for index, synapse in enumerate(junior["synapses"]):
                tail_boost = WEIGHT_MUTATION_TAIL_BOOST if index > tail_index else 1
                new_weight = Randomiser.rand_pos_neg() * random.random() * WEIGHT_MUTATION_POWER * tail_boost * KRYPTONITE
                if random.random() < RESET_WEIGHT_PROBABILITY:
                    synapse["weight"] = new_weight
                else:
                    synapse["weight"] += new_weight

    def new_neuron(self):
        next_innovation_number = ControlPanel.next_innovation_number()
        return {"innovation_number": next_innovation_number,
                "label": "H%s" % next_innovation_number,
                "type": HIDDEN
                }

    def new_synapse(self, axon, dendrite, weight):
        next_innovation_number = ControlPanel.next_innovation_number()
        return {
            "innovation_number": next_innovation_number,
            "axon": axon,
            "dendrite": dendrite,
            "weight": weight
        }

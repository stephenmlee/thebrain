import random
from CommandBunker import ControlPanel
from CommandBunker.ControlPanel import DISJOINT_COEFF, EXCESS_COEFF, MUTATION_DIFF_COEFF, MUTATE_LINKS_PROBABILITY, \
    DISABLE_GENE_PROBABILITY, REENABLE_GENE_PROBABILITY, ADD_NODE_PROBABILITY, ADD_LINK_PROBABILITY, \
    WEIGHT_MUTATION_TAIL_BOOST, WEIGHT_MUTATION_POWER, RESET_WEIGHT_PROBABILITY
from Cranium.Neuron import BIAS, HIDDEN
from EvolutionChamber import Randomiser
from EvolutionChamber.Randomiser import rand_pos_neg

__author__ = 'stephen'


class GeneSplicer(object):
    def __init__(self):
        pass

    def mate(self, mum, dad):
        mum_neurons = mum["neurons"]
        dad_neurons = dad["neurons"]
        mum_synapses = mum["synapses"]
        dad_synapses = dad["synapses"]
        better_fitness = mum if mum["fitness"] > dad["fitness"] else dad
        junior_synapses = []
        junior_neurons = {mum_neuron["label"]: mum_neuron for mum_neuron in mum_neurons if
                          mum_neuron["label"][0] != "H"}
        g1 = 0
        g2 = 0
        while g1 < len(mum_synapses) and g2 < len(dad_synapses):
            if g1 >= len(dad_synapses):
                if better_fitness is mum:
                    junior_synapses.append(mum_synapses[g1])
                    self.mum_neurons(g1, junior_neurons, mum_neurons, mum_synapses[g1])
                g1 += 1
            elif g2 >= len(dad_synapses):
                if better_fitness is not mum:
                    junior_synapses.append(dad_synapses[g2])
                    self.add_dad_neurons(g2, dad_neurons, junior_neurons, dad_synapses[g2])
                g2 += 1
            else:
                innov1 = mum_synapses[g1]["innovation_number"]
                innov2 = dad_synapses[g2]["innovation_number"]
                if innov1 == innov2:
                    if rand_pos_neg() == 1:
                        junior_synapses.append(mum_synapses[g1])
                        self.mum_neurons(g1, junior_neurons, mum_neurons, mum_synapses[g1])

                    else:
                        junior_synapses.append(dad_synapses[g2])
                        self.add_dad_neurons(g2, dad_neurons, junior_neurons, dad_synapses[g2])

                    g1 += 1
                    g2 += 1
                elif innov1 < innov2:
                    if better_fitness is mum:
                        junior_synapses.append(mum_synapses[g1])
                        self.mum_neurons(g1, junior_neurons, mum_neurons, mum_synapses[g1])
                    g1 += 1
                else:
                    if better_fitness is not mum:
                        junior_synapses.append(dad_synapses[g1])
                        self.add_dad_neurons(g2, dad_neurons, junior_neurons, dad_synapses[g2])
                    g2 += 1

        junior = {"id": ControlPanel.next_organism_number(), "fitness": mum["fitness"], "neurons": [], "synapses": []}

        connections = set()
        for i, synapse in enumerate(junior_synapses):
            connection = synapse["axon"] + synapse["dendrite"]
            if connection not in connections:
                connections.add(connection)
                junior["synapses"].append(synapse)
        junior["neurons"].extend(junior_neurons.values())

        return junior

    def add_dad_neurons(self, g2, dad_neurons, junior_neurons, dad_synapses):
        axons = filter(lambda n: n["label"] == dad_synapses["axon"] and n["label"][0] == "H", dad_neurons)
        if len(axons) > 0:
            junior_neurons[dad_synapses["axon"]] = axons[0]
        dendrites = filter(lambda n: n["label"] == dad_synapses["dendrite"], dad_neurons)
        if len(dendrites) > 0:
            junior_neurons[dad_synapses["dendrite"]] = dendrites[0]

    def mum_neurons(self, g1, junior_neurons, mum_neurons, mum_synapses):
        axons = filter(lambda n: n["label"] == mum_synapses["axon"] and n["label"][0] == "H", mum_neurons)
        if len(axons) > 0:
            junior_neurons[mum_synapses["axon"]] = axons[0]
        dendrites = filter(lambda n: n["label"] == mum_synapses["dendrite"], mum_neurons)
        if len(dendrites) > 0:
            junior_neurons[mum_synapses["dendrite"]] = dendrites[0]

    def compatibility_scan(self, genome1, genome2):
        genes1 = genome1["synapses"]
        genes2 = genome2["synapses"]
        g1 = 0
        g2 = 0
        num_excess = 0
        num_disjoint = 0
        num_matching = 0
        mutation_difference = 0

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

        return (DISJOINT_COEFF * num_disjoint) + (EXCESS_COEFF * num_excess) \
               + (MUTATION_DIFF_COEFF * (mutation_difference / num_matching))

    def mutate(self, junior):
        KRYPTONITE = 1
        if random.random() < 0.01:
            KRYPTONITE = 5

        if random.random() < DISABLE_GENE_PROBABILITY:
            synapse_genes = junior["synapses"]
            random_gene = synapse_genes[random.randint(0, len(synapse_genes) - 1)]
            random_gene["disabled"] = "true"

        elif random.random() < ADD_LINK_PROBABILITY:
            neurons = junior["neurons"]
            random_neuron_1 = neurons[random.randint(0, len(neurons) - 1)]
            random_neuron_2 = neurons[random.randint(0, len(neurons) - 1)]

            link_exists = False
            for synapse in junior["synapses"]:
                if synapse["axon"] == random_neuron_1["label"] and synapse["dendrite"] == random_neuron_2["label"]:
                    link_exists = True

            if not link_exists and random_neuron_2["type"] not in ["Sensor", "Bias"] \
                    and (not (random_neuron_1["type"] == "Hidden" and random_neuron_2["type"] == "Hidden")
                         or random_neuron_1["label"] == random_neuron_2["label"]):
                junior["synapses"].append(self.new_synapse(random_neuron_1["label"], random_neuron_2["label"], 1))

        elif random.random() < ADD_NODE_PROBABILITY:
            synapse_genes = junior["synapses"]
            random_gene = synapse_genes[random.randint(0, len(synapse_genes) - 1)]

            old_dendrite = random_gene["dendrite"]
            old_axon = random_gene["axon"]

            if old_axon[:1] in ["S", "H"] and not (old_axon[:1] == "H" and old_dendrite[:1] == "H"):
                random_gene["disabled"] = "true"
                new_neuron = self.new_neuron()
                junior["neurons"].append(new_neuron)
                junior["synapses"].append(self.new_synapse(old_axon, new_neuron["label"], 1))
                junior["synapses"].append(self.new_synapse(new_neuron["label"], old_dendrite, random_gene["weight"]))

        elif random.random() < MUTATE_LINKS_PROBABILITY:
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

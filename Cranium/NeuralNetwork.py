from Cranium.Synapse import Synapse
from Cranium.Neuron import SensorNeuron, HiddenNeuron, BiasNeuron, OutputNeuron, OUTPUT, SENSOR, HIDDEN, BIAS

MAX_RELAX_COUNT = 30


class NeuralNetwork(object):

    def __init__(self, id=0):
        self.id = 0
        self.neurons = {}

    def stimulate(self, input_values):
        for sensor, activation in input_values:
            self.neurons[sensor].load_stimuli(activation)

    def electrify(self):
        relax_count = 0
        while not self.relaxed():
            if relax_count > MAX_RELAX_COUNT:
                raise UnstableNetworkError()
            relax_count += 1
            for neuron in self.neurons.itervalues():
                neuron.load()
            for neuron in self.neurons.itervalues():
                neuron.zapp()

    def outputs(self):
        return {label: neuron for label, neuron in self.neurons.iteritems() if neuron.type == OUTPUT}

    def add_sensor_node(self, innov_num, label):
        self.neurons[label] = SensorNeuron(innov_num, label)

    def add_hidden_node(self, innov_num, label):
        self.neurons[label] = HiddenNeuron(innov_num, label)

    def add_bias_node(self, innov_num, label):
        self.neurons[label] = BiasNeuron(innov_num, label)

    def add_output_node(self, innov_num, label):
        self.neurons[label] = OutputNeuron(innov_num, label)

    def connect(self, innovation_number, source, receiver, weight):
        try:
            synapse = Synapse(innovation_number, weight, self.neurons[source], self.neurons[receiver])
            self.neurons[receiver].splice_dendrite_to(synapse)
        except KeyError:
            pass

    def relaxed(self):
        for neuron in self.neurons.itervalues():
            if not neuron.is_relaxed():
                return False
        return True

    def decode_genome(self):
        neurons = []
        synapses = []
        for neuron in self.neurons.itervalues():
            neurons.append(neuron.decode_genome())
            for synapse in neuron.dendrites:
                synapses.append(synapse.decode_genome())

        neurons.sort(key=lambda n: n["innovation_number"])
        synapses.sort(key=lambda s: s["innovation_number"])

        return {"id": self.id, "neurons": neurons, "synapses": synapses}


def expressed_from(genome):
    network = NeuralNetwork(id)

    for gene in genome["neurons"]:
        innov_num = gene["innovation_number"]
        label = gene["label"]

        if gene["type"] == SENSOR:
            network.add_sensor_node(innov_num, label)
        elif gene["type"] == HIDDEN:
            network.add_hidden_node(innov_num, label)
        elif gene["type"] == BIAS:
            network.add_bias_node(innov_num, label)
        elif gene["type"] == OUTPUT:
            network.add_output_node(innov_num, label)

    for gene in genome["synapses"]:
        if gene.get("disabled") is None:
            network.connect(gene["innovation_number"], gene["axon"], gene["dendrite"], gene["weight"])

    return network

class UnstableNetworkError(Exception):
    pass

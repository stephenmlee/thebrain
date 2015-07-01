import math

__author__ = 'stephen'

SENSOR = "Sensor"
HIDDEN = "Hidden"
OUTPUT = "Output"
BIAS = "Bias"


class Neuron(object):
    def __init__(self, innovation_number, label, type):
        self.innovation_number = innovation_number
        self.label = label
        self.type = type
        self.dendrites = []
        self.incoming_activation = None
        self.outgoing_activation = None
        self.prior_outgoing_activation = None

    def splice_dendrite_to(self, synapse):
        self.dendrites.append(synapse)

    def is_relaxed(self):
        return self.outgoing_activation == self.prior_outgoing_activation

    def load(self):
        self.incoming_activation = sum([synapse.weighted_activation() for synapse in self.dendrites
                                        if synapse.weighted_activation() is not None])

    def activation(self):
        return self.outgoing_activation

    def zapp(self):
        self.prior_outgoing_activation = self.outgoing_activation
        self.outgoing_activation = self._sigmoid(self.incoming_activation)

    def decode_genome(self):
        return {"innovation_number": self.innovation_number, "label": self.label, "type": self.type}

    def _sigmoid(self, x):
        return 1 / (1 + math.exp(-4.924273 * x))


class SensorNeuron(Neuron):
    def __init__(self, innovation_number, label):
        super(SensorNeuron, self).__init__(innovation_number, label, SENSOR)

    def load_stimuli(self, activation):
        self.incoming_activation = self.outgoing_activation = activation

    def zapp(self):
        self.prior_outgoing_activation = self.outgoing_activation  # ensures at least one relaxation iteration


class HiddenNeuron(Neuron):
    def __init__(self, innovation_number, label):
        super(HiddenNeuron, self).__init__(innovation_number, label, HIDDEN)


class OutputNeuron(Neuron):
    def __init__(self, innovation_number, label):
        super(OutputNeuron, self).__init__(innovation_number, label, OUTPUT)


class BiasNeuron(Neuron):
    def __init__(self, innovation_number, label):
        super(BiasNeuron, self).__init__(innovation_number, label, BIAS)
        self.outgoing_activation = self.prior_outgoing_activation = 1

    def zapp(self):
        pass

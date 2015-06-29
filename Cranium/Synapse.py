class Synapse(object):
    def __init__(self, innovation_number, weight, axon_neuron, dendrite_neuron):
        self.innovation_number = innovation_number
        self.weight = weight
        self.axon = axon_neuron
        self.dendrite = dendrite_neuron

    def weighted_activation(self):
        if self.axon.activation():
            return self.axon.activation() * self.weight

    def decode_genome(self):
        return {"innovation_number": self.innovation_number,
                "axon": self.axon.label,
                "dendrite": self.dendrite.label,
                "weight": self.weight}

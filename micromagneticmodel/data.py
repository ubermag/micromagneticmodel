class Data:
    def __init__(self, system, interaction):
        self.system = system
        self.interaction = interaction

    @property
    def energy(self):
        raise NotImplementedError

    @property
    def energy_density(self):
        raise NotImplementedError

    @property
    def effective_field(self):
        raise NotImplementedError

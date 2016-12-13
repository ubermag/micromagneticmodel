class Data:
    @property
    def energy(self):
        raise NotImplementedError

    @property
    def energy_density(self):
        raise NotImplementedError

    @property
    def effective_field(self):
        raise NotImplementedError

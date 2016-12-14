class Data:
    def __init__(self, system, cls):
        self.system = system
        self.cls = cls

    @property
    def energy(self):
        raise NotImplementedError

    @property
    def energy_density(self):
        raise NotImplementedError

    @property
    def effective_field(self):
        raise NotImplementedError

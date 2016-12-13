import importlib


class EnergyProperties:
    @property
    def energy(self):
        raise NotImplementedError

    @property
    def energy_density(self):
        raise NotImplementedError

    @property
    def effective_field(self):
        selfmodule = importlib.__import__(self.__class__.__module__)
        data = selfmodule.Data(self.termsum.system, self.__class__.__name__)
        return data.effective_field

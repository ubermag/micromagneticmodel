import importlib


class EnergyProperties:
    @property
    def data(self):
        selfmodule = importlib.__import__(self.__class__.__module__)
        if self.__class__.__name__ == "Hamiltonian":
            return selfmodule.Data(self.system, self.__class__.__name__)
        else:
            return selfmodule.Data(self.termsum.system, self.__class__.__name__)
    
    @property
    def energy(self):
        return self.data.energy

    @property
    def energy_density(self):
        return self.data.energy_density

    @property
    def effective_field(self):
        return self.data.effective_field

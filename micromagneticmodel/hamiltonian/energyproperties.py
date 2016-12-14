import importlib


class EnergyProperties:
    @property
    def _data(self):
        module = importlib.__import__(self.__class__.__module__)
        if self.__class__.__name__ == "Hamiltonian":
            system = self._system
        else:
            system = self._termsum._system
        return module.Data(system, self.__class__.__name__)

    @property
    def energy(self):
        return self._data.energy

    @property
    def energy_density(self):
        return self._data.energy_density

    @property
    def effective_field(self):
        return self._data.effective_field

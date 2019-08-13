import importlib


class EnergyProperties:
    """Energy properties class inherited by all energy terms and
    Hamiltonian used for deriving energy, energy density, and
    effective field.

    """
    @property
    def _data(self):
        """Returns `micromagneticmodel.Data` object, which is able to compute
        energy, energy density, and effective field.

        """
        module = importlib.__import__(self.__class__.__module__)
        if self.__class__.__name__ == "Hamiltonian":
            system = self._system
        else:
            system = self._termsum._system
        return module.Data(system, self.__class__.__name__)

    @property
    def energy(self):
        """Energy.

        Returns
        -------
        float
            Energy

        """
        return self._data.energy

    @property
    def energy_density(self):
        """Energy density.

        Returns
        -------
        df.Field
            Scalar (dim=1) field.

        """
        return self._data.energy_density

    @property
    def effective_field(self):
        """Effective field.

        Returns
        -------
        df.Field
            Vector (dim=3) field.

        """
        return self._data.effective_field

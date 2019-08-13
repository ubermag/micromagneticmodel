class Data:
    """Data class used for deriving energy, energy density, and effective
    field.

    This class should be inherited and methods `energy`,
    `energy_density`, and `effective_field` implemented by a derived
    class.

    """
    def __init__(self, system, cls):
        self.system = system
        self.cls = cls

    @property
    def energy(self):
        """Energy.

        This method should be implemented by a derived class. It is
        expected to return a scalar.

        """
        raise NotImplementedError

    @property
    def energy_density(self):
        """Energy density.

        This method should be implemented by a derived class. It is
        expected to return a scalar field object.

        """
        raise NotImplementedError

    @property
    def effective_field(self):
        """Effective field.

        This method should be implemented by a derived class. It is
        expected to return a vector field object.

        """
        raise NotImplementedError

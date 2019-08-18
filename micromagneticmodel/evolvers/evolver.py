class Evolver:
    def __init__(self, **kwargs):
        """Evolver class.

        Different evolver classes are derived from this one. This
        class accepts any keyword argument that could be required by a
        derived evolver.

        """
        self.__dict__.update(kwargs)

    @property
    def _script(self):
        """Script property.

        This method should be implemented by a specific micromagnetic
        caclulator.

        """
        raise NotImplementedError

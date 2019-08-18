class Evolver:
    _allowed_kwargs = []

    def __init__(self, **kwargs):
        """Evolver class.

        Different evolver classes are derived from this one. This
        class accepts any keyword argument that could be required by a
        derived evolver.

        """
        for key, value in kwargs.items():
            if key in self._allowed_kwargs:
                self.__dict__[key] = value
            else:
                msg = f'Attribute {key} is not allowed.'
                raise AttributeError(msg)

    @property
    def _script(self):
        """Script property.

        This method should be implemented by a specific micromagnetic
        caclulator.

        """
        raise NotImplementedError

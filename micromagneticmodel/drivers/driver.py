class Driver:
    _allowed_kwargs = []

    def __init__(self, **kwargs):
        """Driver class.

        Different driver classes are derived from this one. This class
        accepts any keyword argument that could be required by a
        derived driver.

        """
        for key, value in kwargs.items():
            if key in self._allowed_kwargs:
                self.__dict__[key] = value
            else:
                msg = f'Attribute {key} is not allowed.'
                raise AttributeError(msg)

    def drive(self):
        """Drive method.

        This method should be implemented by a specific micromagnetic
        caclulator.

        """
        raise NotImplementedError

    @property
    def _script(self):
        """Script property.

        This method should be implemented by a specific micromagnetic
        caclulator.

        """
        raise NotImplementedError

class Driver:
    def __init__(self, **kwargs):
        """Driver class.

        Different driver classes (`micromagneticmodel.TimeDriver`,
        `micromagneticmodel.MinDriver`, and
        `micromagneticmodel.HysteresisDriver`) are derived from this
        one. This class accepts any keyword argument that could be
        required by a derived driver.

        """
        self.__dict__.update(kwargs)

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

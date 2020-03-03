import abc


class Driver(metaclass=abc.ABCMeta):
    def __init__(self, **kwargs):
        """It can be initialised with keyword arguments defined in
        ``_allowed_attributes``, which is a list of strings.

        Raises
        ------
        ValueError

            If a keyword argument not in ``_allowed_attributes`` is passed.

        """
        for key, value in kwargs.items():
            if key in self._allowed_attributes:
                setattr(self, key, value)
            else:
                msg = f'Invalid attribute {key} for {self.__class__}.'
                raise AttributeError(msg)

    @property
    @abc.abstractmethod
    def _allowed_attributes(self):
        """A list of attributes allowed to be set at initialisation by passing
        keyword arguments.

        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def drive(self):
        """Drive method.

        This method should be implemented by a specific micromagnetic
        caclulator.

        """
        pass  # pragma: no cover

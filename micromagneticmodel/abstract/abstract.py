import abc

import ubermagutil.typesystem as ts


class Abstract(metaclass=abc.ABCMeta):
    """Abstract class for deriving all terms, drivers, and evolvers.

    It can be initialised with keyword arguments defined in
    ``_allowed_attributes``, which is a list of strings.

    Raises
    ------
    AttributeError

        If a keyword argument not in ``_allowed_attributes`` is passed.

    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._allowed_attributes or key == "name":
                setattr(self, key, value)
            else:
                msg = f"Invalid attribute {key=} for {self.__class__=}."
                raise AttributeError(msg)

    @property
    @abc.abstractmethod
    def _allowed_attributes(self):
        """A list of attributes allowed to be set at initialisation by passing
        keyword arguments.

        """
        pass  # pragma: no cover

    def __iter__(self):
        """Iterator.

        It yields all defined attributes and their values.

        Examples
        --------
        1. Iterating through all defined attributes and their values.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1)
        >>> for attr, value in exchange:
        ...     print(f'{attr} = {value}')
        A = 1

        """
        for attr in self._allowed_attributes:
            if hasattr(self, attr):
                yield attr, getattr(self, attr)

    def __repr__(self):
        """Representation string.

        Returns
        -------
        str

            Representation string.

        Examples
        --------
        1. Getting representation string.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> repr(exchange)
        'Exchange(A=1e-12)'
        >>> damping = mm.Damping(alpha=0.01)
        >>> repr(damping)
        'Damping(alpha=0.01)'

        """
        attributes = []
        for attr, value in self:
            if isinstance(value, str):
                attributes.append(f"{attr}='{value}'")
            elif not isinstance(value, ts.Descriptor):
                # The parameter is not set.
                attributes.append(f"{attr}={value}")
        attributes = ", ".join(attributes)
        return f"{self.__class__.__name__}({attributes})"

    @property
    def name(self):
        """Name.

        If the name was not provided during initialisation, the name of the
        object is the same as the name of the class in lowercase.

        Returns
        -------
        str

            Name.

        Examples
        --------
        1. Getting names.

        >>> import micromagneticmodel as mm
        ...
        >>> ua = mm.UniaxialAnisotropy(K=5e6, u=(0, 0, 1))
        >>> ua.name
        'uniaxialanisotropy'
        >>> damping = mm.Damping(alpha=0.01, name='my_damping')
        >>> damping.name
        'my_damping'

        """
        if hasattr(self, "_name"):
            return self._name
        else:
            return self.__class__.__name__.lower()

    @name.setter
    def name(self, value):
        self._name = value

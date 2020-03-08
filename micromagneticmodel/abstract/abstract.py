import abc


class Abstract(metaclass=abc.ABCMeta):
    """An abstract class for deriving all energy and dynamics terms as well as
    driver and evolver classes.

    """
    def __init__(self, **kwargs):
        """It can be initialised with keyword arguments defined in
        ``_allowed_attributes``, which is a list of strings.

        Raises
        ------
        AttributeError

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

    def __iter__(self):
        """Iterator.

        It yields all defined attributes and their values.

        Examples
        --------
        1. Iterating through all defined attributes and their values.

        >>> import micromagneticmodel as mm
        ...
        >>> uniaxialanisotropy = mm.UniaxialAnisotropy(K=1e5, u=(0, 0, 1))
        >>> for attr, value in uniaxialanisotropy:
        ...     print(f'{attr} = {value}')
        K = 100000.0
        u = (0, 0, 1)

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
        >>> zeeman = mm.Zeeman(H=(100, 0, 0))
        >>> repr(zeeman)
        'Zeeman(H=(100, 0, 0))'
        >>> damping = mm.Damping(alpha=0.01)
        >>> repr(damping)
        'Damping(alpha=0.01)'

        """
        attributes = []
        for attr, value in self:
            if isinstance(value, str):
                attributes.append(f'{attr}=\'{value}\'')
            else:
                attributes.append(f'{attr}={value}')
        attributes = ', '.join(attributes)
        return f'{self.__class__.__name__}({attributes})'

    @property
    def name(self):
        """Name.

        The name of the object is the same as the name of the class in
        lowercase.

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
        >>> damping = mm.Damping(alpha=0.01)
        >>> damping.name
        'damping'

        """
        return self.__class__.__name__.lower()

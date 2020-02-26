import abc
import micromagneticmodel as mm


class Term(metaclass=abc.ABCMeta):
    """An abstract class for deriving all energy and dynamics terms.

    """
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
                raise ValueError(msg)

    @property
    @abc.abstractmethod
    def _allowed_attributes(self):
        """A list of attributes allowed to be set at initialisation by passing
        keyword arguments.

        """
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _container_class(self):
        """A class of a container, which is the result of adding terms.

        """
        pass  # pragma: no cover

    def __eq__(self, other):
        """Relational operator ``==``.

        Two terms are considered to be equal if they are instances of the same
        class.

        Parameters
        ----------
        other : micromagneticmodel.Term

            Second operand.

        Returns
        -------
        bool

            ``True`` if two terms are instances of the same class and ``False``
            otherwise.

        Examples
        --------
        1. Comparing terms.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> zeeman = mm.Zeeman(H=(0, 0, 1e6))
        >>> damping = mm.Damping(alpha=0.1)
        >>> demag = mm.Demag()
        ...
        >>> exchange == exchange
        True
        >>> exchange == mm.Exchange(A=5e-11)  # only class is checked
        True
        >>> zeeman != exchange
        True
        >>> zeeman == exchange
        False
        >>> damping == damping
        True
        >>> damping != exchange
        True
        >>> demag == exchange
        False

        """
        if isinstance(other, self.__class__):
            return True
        else:
            return False

    def __add__(self, other):
        """Binary ``+`` operator.

        It can be applied only between two ``micromagneticmodel.util.Term``
        objects.

        Parameters
        ----------
        other : micromagneticmodel.util.Term

            Second operand.

        Returns
        -------
        micromagneticmodel.util.Container

            Resulting sum.

        Examples
        --------
        1. Adding energy terms.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> demag = mm.Demag()
        ...
        >>> container = exchange + demag
        >>> type(container)
        <class 'micromagneticmodel.energy.energy.Energy'>

        2. Adding dynamics terms.

        >>> precession = mm.Precession(gamma=mm.consts.gamma0)
        >>> damping = mm.Damping(alpha=0.01)
        ...
        >>> container = precession + damping
        >>> type(container)
        <class 'micromagneticmodel.dynamics.dynamics.Dynamics'>

        """
        result = getattr(mm, self._container_class)()
        result += self
        result += other
        return result

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
        for attr in self._allowed_attributes:
            if hasattr(self, attr):
                if isinstance(getattr(self, attr), str):
                    attributes.append(f'{attr}=\'{getattr(self, attr)}\'')
                else:
                    attributes.append(f'{attr}={getattr(self, attr)}')
        attributes = ', '.join(attributes)
        return f'{self.__class__.__name__}({attributes})'

    @property
    @abc.abstractmethod
    def _reprlatex(self):
        """"LaTeX representation abstract method, rendered inside Jupyter and
        returned by ``micromagneticmodel.Term._repr_latex_``.

        """
        pass  # pragma: no cover

    def _repr_latex_(self):
        """"LaTeX representation method, rendered in Jupyter. This method has
        the priority over ``__repr__`` in Jupyter.

        Returns
        -------
        str

            LaTeX representation string.

        Examples
        --------
        1. Getting LaTeX representation string.

        >>> import micromagneticmodel as mm
        ...
        >>> zeeman = mm.Zeeman(H=(100, 0, 0))
        >>> zeeman._repr_latex_()
        '$-\\\\mu_{0}M_\\\\text{s} \\\\mathbf{m} \\\\cdot \\\\mathbf{H}$'
        >>> # zeeman  # inside Jupyter

        """
        return f'${self._reprlatex}$'

    @property
    def name(self):
        """Name.

        Used for accessing individual terms from
        ``micromagneticmodel.Container`` objects. The name of the object is the
        same as the name of the class in lowercase.

        Returns
        -------
        str

            Term name.

        Examples
        --------
        1. Getting term names.

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

import abc
import micromagneticmodel as mm


class Term(metaclass=abc.ABCMeta):
    """An abstract class for deriving all energy and dynamics terms.

    It can be initialised with keyword arguments defined in
    ``_allowed_attributes``, which is a list of strings.

    Raises
    ------
    ValueError

        If a keyword argument not in ``_allowed_attributes`` is passed.

    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._allowed_attributes:
                setattr(self, key, value)
            else:
                msg = f'Invalid attribute {key} for {self.__class__}.'
                raise ValueError(msg)

    @property
    @abc.abstractmethod
    def _allowed_attributes(self):
        """A list of attributes allowed to be set at initialisation.

        """
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _termscontainer_class(self):
        """A class of an object, which is the result of adding terms.

        """
        pass  # pragma: no cover

    def __eq__(self, other):
        """Relational operator ``==``.

        Two terms are considered to be equal if all attributes in
        ``_allowed_attributes`` are equal.

        Parameters
        ----------
        other : micromagneticmodel.Term

            Second operand.

        Returns
        -------
        bool

            ``True`` if two terms are equal and ``False`` otherwise.

        Examples
        --------
        1. Comparing terms.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> zeeman = mm.Zeeman(H=(0, 0, 1e6))
        >>> exchange == exchange
        True
        >>> exchange == mm.Exchange(A=5e-11)
        False
        >>> zeeman != exchange
        True
        >>> zeeman == exchange
        False

        """
        if not isinstance(other, self.__class__):
            return False
        if all([getattr(self, attr) == getattr(other, attr)]
               for attr in self._allowed_attributes):
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
        micromagneticmodel.util.TermSum

            Resulting sum.

        Examples
        --------
        1. Adding energy terms.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> demag = mm.Demag()
        ...
        >>> terms_sum = exchange + demag
        >>> type(terms_sum)
        Energy

        2. Adding dynamics terms.

        >>> import micromagneticmodel as mm
        ...
        >>> precession = mm.Precession(gamma=mm.consts.gamma0)
        >>> damping = mm.Damping(alpha=0.01)
        ...
        >>> terms_sum = precession + damping
        >>> type(terms_sum)
        Dynamics

        """
        result = getattr(mm, self._termscontainer_class)()
        result += self
        result += other

        return result

    @abc.abstractmethod
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
        ...
        >>> damping = mm.Damping(alpha=0.01)
        >>> repr(damping)
        'Damping(alpha=0.01)'

        """
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _reprlatex(self):
        """"LaTeX representation abstract method, rendered inside Jupyter and
        returned by ``micromagneticmodel.Term._repr_latex_``.

        """
        pass  # pragma: no cover

    def _repr_latex_(self):
        """"LaTeX representation method, rendered inside Jupyter. This method
        has the priority over ``__repr__`` in Jupyter.

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
        >>> zeeman._latex_repr_()
        '-\\mu_{0}M_\\text{s} \\mathbf{m} \\cdot \\mathbf{H}'
        >>> # zeeman  # inside Jupyter

        """
        return f'${self._reprlatex}$'

    @property
    def name(self):
        """Name.

        Used for accessing individual terms from ``micromagneticmodel.TermSum``
        objects. The name of the object is the same as the name of the class in
        lowercase.

        Returns
        -------
        str

            Term name.

        Examples
        --------
        1. Getting term names.

        >>> import micromagneticmodel as mm
        ...
        >>> ua = mm.UniaxialAnisotropy(K1=5e6, u=(0, 0, 1))
        >>> ua.name
        'uniaxialanisotropy'
        ...
        >>> damping = mm.Damping(alpha=0.01)
        >>> damping.name
        'damping'

        """
        return self.__class__.__name__.lower()

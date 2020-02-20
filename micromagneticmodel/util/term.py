import abc


class Term(metaclass=abc.ABCMeta):
    """An abstract class for deriving both energy and dynamics terms.

    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in self._allowed_attributes:
                setattr(self, k, v)
            else:
                msg = f'Invalid attribute {k} for {self.__class__}.'
                raise ValueError(msg)

    @property
    @abc.abstractmethod
    def _allowed_attributes(self):
        """A list of attributes allowed to be set by the user.

        """
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _termsum_type(self):
        """A class of an object obtained as the result of adding terms.

        """
        pass  # pragma: no cover

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

        Raises
        ------
        TypeError

            If the operator cannot be applied.

        """
        termsum = self._termsum_type()
        termsum += self
        termsum += other
        return termsum

    def __radd__(self, other):
        return other + self

    def __eq__(self, other):
        """Relational operator ``==``.

        Two terms are considered to be equal if all attributes in
        ``_allowed_attrs`` are equal.

        ``name`` is not considered to be a necessary condition for equality.

        Parameters
        ----------
        other : micromagneticmodel.TermSum

            Term compared to ``self``.

        Returns
        -------
        bool

            ``True`` if two terms are equal and ``False`` otherwise.

        Example
        -------
        1. Check if terms are equal.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange1 = mm.Exchange(A=1e-12)
        >>> exchange2 = mm.Exchange(A=1e-12, name='myexchange')
        >>> exchange2 = mm.Exchange(A=2e-12)
        >>> precession1 = mm.Precession(gamma0=mm.gamma0)
        >>> exchange1 == exchange2  # name is not checked for equality
        True
        >>> exchange1 == exchange3
        False
        >>> exchange1 != exchange3
        True
        >>> exchange1 == precession1
        False
        >>> exchange1 != precession1

        """
        if not isinstance(other, self.__class__):
            return False
        if all(getattr(self, attr) == getattr(other, attr)
               for attr in self._allowed_attrs if attr != 'name'):
            return True
        else:
            return False

    @property
    @abc.abstractmethod
    def _reprlatex(self):
        """"LaTeX representation abstract method, rendered inside Jupyter. This
        method has the priority over ``__repr__`` in Jupyter.

        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def __repr__(self):
        """Representation string abstract method.

        """
        pass

    @abc.abstractmethod
    def _repr_latex_(self):
        """"LaTeX representation abstract method, rendered inside Jupyter. This
        method has the priority over ``__repr__`` in Jupyter.

        Returns
        -------
        str

            LaTeX representation string.

        Example
        -------
        1. Get LaTeX representation string.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> exchange._repr_latex_()
        '$A (\\nabla \\mathbf{m})^{2}$'

        """
        pass  # pragma: no cover

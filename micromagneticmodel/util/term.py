import abc
import micromagneticmodel as mm


class Term(metaclass=abc.ABCMeta):
    """An abstract class for deriving all energy and dynamics terms.

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
        """A list of attributes allowed to be set by the user.

        """
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _termsum_type(self):
        """A class of an object obtained as the result of adding terms.

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

        """
        if not isinstance(other, self.__class__):
            return False
        if all(all([getattr(self, attr) == getattr(other, attr)])
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

        Raises
        ------
        TypeError

            If the operator cannot be applied.

        """
        result = getattr(mm, self._termsum_type)()
        result += self
        result += other

        return result

    def __radd__(self, other):
        return other + self  # is this necessary?

    @abc.abstractmethod
    def __repr__(self):
        """Representation string.

        Returns
        -------
        str

            Representation string.

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

        """
        return f'${self._reprlatex}$'

    @property
    def name(self):
        """Name.

        Used for accessing individual terms from ``micromagneticmodel.TermSum``
        objects.

        Returns
        -------
        str

            Term name.

        """
        return self.__class__.__name__.lower()

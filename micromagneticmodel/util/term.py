import abc


class Term(metaclass=abc.ABCMeta):
    """An abstract class for deriving terms.

    """
    @abc.abstractmethod
    def __init__(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def __repr__(self):
        """Representation string abstract method.

        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def _repr_latex_(self):
        """"LaTeX representation abstract method, rendered inside Jupyter.

        """
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _termsum_type(self):
        """A class which is the result of term addition.

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
        if not isinstance(other, self.__class__):
            msg = (f'Unsupported operand type(s) for +: '
                   f'{type(self)} and {type(other)}.')
            raise TypeError(msg)
        termsum = self._termsum_type()
        termsum += self
        termsum += other
        return termsum

    def __radd__(self, other):
        return other + self

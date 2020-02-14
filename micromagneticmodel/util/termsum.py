import abc


class TermSum(metaclass=abc.ABCMeta):
    """An abstract class for deriving term sums.

    """
    def __init__(self):
        self.terms = []

    def __repr__(self):
        """Representation string method.

        Returns
        -------
        str

            Representation string.

        """
        return ' + '.join([repr(term) for term in self.terms])

    def _repr_latex_(self):
        """LaTeX representation abstract method, rendered inside Jupyter.

        Returns
        -------
        str

            LaTeX representation string.

        """
        reprlatex = self._lefthandside
        if not self.terms:
            reprlatex += '0$'
        else:
            for term in self.terms:
                termlatex = term._repr_latex_()
                termlatex = termlatex.replace('$', '')
                if termlatex[0] != '-':
                    reprlatex += f'+ {termlatex}'
            reprlatex += '$'

        return reprlatex

    @property
    @abc.abstractmethod
    def _lefthandside(self):
        """Lefthandside of the LaTeX representation string.

        """
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _terms_type(self):
        """A class which can be added to ``TermSum``.

        """
        pass  # pragma: no cover

    def __add__(self, value):
        """Binary ``+`` operator.

        It can be applied only between two ``micromagneticmodel.util.TermSum``
        objects or between ``micromagneticmodel.util.TermSum`` and
        ``micromagneticmodel.util.Term``.

        Parameters
        ----------
        other : micromagneticmodel.util.Term, micromagneticmodel.util.TermSum

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
        if isinstance(value, self._terms_type):
            setattr(value, '_termsum', self)  # to track who it belongs to
            self.terms.append(value)
            setattr(self, value.name, value)  # to make it accessible by name
        elif isinstance(value, self.__class__):
            for term in value.terms:
                self += term
        else:
            msg = (f'Unsupported operand type(s) for +: '
                   f'{type(self)} and {type(other)}.')
            raise TypeError(msg)

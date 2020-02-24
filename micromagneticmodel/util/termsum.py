import abc


class TermSum(metaclass=abc.ABCMeta):
    """An abstract class for deriving term sums.

    """
    def __init__(self):
        self._terms = list()

    def __repr__(self):
        """Representation string method.

        Returns
        -------
        str

            Representation string.

        """
        return ' + '.join([repr(term) for term in self])

    def _repr_latex_(self):
        """LaTeX representation abstract method, rendered inside Jupyter.

        Returns
        -------
        str

            LaTeX representation string.

        """
        reprlatex = self._lefthandside
        if not self._terms:
            reprlatex += '0'
        else:
            for term in self:
                termlatex = term._reprlatex
                if not termlatex.startswith('-'):
                    reprlatex += f'+ {termlatex}'
                else:
                    reprlatex += termlatex

        return f'${reprlatex}$'

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

    def __len__(self):
        return len(self._terms)

    def __iter__(self):
        for term in self._terms:
            yield term

    def __contains__(self, item):
        for term in self:
            if term.name == item.name:
                return True
        else:
            return False

    def __getattr__(self, attr):
        for term in self:
            if attr == term.name:
                return term
        else:
            msg = f'Object has no attribute {attr}.'
            raise AttributeError(msg)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if len(self) == len(other) and \
          all(term in self for term in other):
            return True
        else:
            return False

    def __dir__(self):
        dirlist = dir(self.__class__)
        for term in self:
            dirlist.append(term.name)

        return dirlist

    def __add__(self, other):
        """Binary ``+`` operator.

        It can be applied only between ``micromagneticmodel.util.Term`` or
        ``micromagneticmodel.util.TermSum`` objects.

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
        result = self.__class__()
        for term in self:
            result._terms.append(term)

        if isinstance(other, self._terms_type):
            if other in result:
                msg = f'Cannot have two {other.__class__} terms in the sum.'
                raise ValueError(msg)
            result._terms.append(other)
        elif isinstance(other, self.__class__):
            for term in other:
                result += term
        else:
            msg = (f'Unsupported operand type(s) for +: '
                   f'{type(self)} and {type(other)}.')
            raise TypeError(msg)

        return result

    def __sub__(self, other):
        """Binary ``-`` operator.

        It can be applied only between ``micromagneticmodel.util.Term`` or
        ``micromagneticmodel.util.TermSum`` objects.

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
        result = self.__class__()
        for term in self:
            result._terms.append(term)

        if isinstance(other, self._terms_type):
            if other not in result:
                msg = f'Term {other.__class__} not in {self.__class__}.'
                raise ValueError(msg)
            for term in result:
                if term.name == other.name:
                    result._terms.remove(term)
        elif isinstance(other, self.__class__):
            for term in other:
                result -= term
        else:
            msg = (f'Unsupported operand type(s) for +: '
                   f'{type(self)} and {type(other)}.')
            raise TypeError(msg)

        return result

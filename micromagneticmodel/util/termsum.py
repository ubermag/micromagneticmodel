import abc


class TermSum(metaclass=abc.ABCMeta):
    """An abstract class for the implementation of sum classes of
    individual terms.

    This class should be inherited by a class which implements a
    particular energy or dynamics term.

    """
    def __init__(self):
        self.terms = []

    @property
    @abc.abstractmethod
    def _lefthandside(self):
        """LaTeX representation string of the `TermSum`.

        It is used to construct the representation LaTeX string
        returned by `_repr_latex` method inside Jupyter notebook. It
        describes the left hand side of the expression. This should be
        implemented in a derived class. It can be implemented as a
        global class attribute - it does not have to be a property.

        """
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _terms_type(self):
        """A class which the summed terms are type of.

        This should be implemented in a derived class. It can be
        implemented as a global class attribute - it does not have to
        be a property. For instance, for
        `micromagneticmodel.Hamiltonian`, this would be an
        `micromagneticmodel.EnergyTerm`.

        """
        pass  # pragma: no cover

    @property
    def _repr(self):
        """Representation string returned by `__repr__` method.

        """
        terms_repr = [term._repr for term in self.terms]
        return ' + '.join(terms_repr)

    @property
    def _latex(self):
        """Representation string returned by `_repr_latex` method inside
        Jupyter notebook.

        """
        s = self._lefthandside
        for term in self.terms:
            if term._latex[1] != '-' and s[-1] != '=':
                s += '+'
            s += term._latex[1:-1]
        if self.terms == []:
            s += '0'
        s += '$'

        return s

    def __repr__(self):
        """Representation string.

        This method returns the string that can be copied in another
        Python script so that exactly the same mesh object could be
        defined.

        Returns
        -------
        str
            Representation string.

        """
        return self._repr

    def _repr_latex_(self):
        """LaTeX representation string.

        This method returns the string that can be rendered as LaTeX
        representation of the object.

        Returns
        -------
        str
            LaTeX representation string.

        """
        return self._latex

    def _add(self, value):
        """Addition operation.

        This method is called when `micromagneticmodel.util.Term` or
        `micromagneticmodel.util.TermSum` to `self`.

        Parameters
        ----------
        other : micromagneticmodel.util.Term or TermSum
            A term or term sum which should be added to `self`.

        Raises
        ------
        TypeError
            If wrong term is attempted to be added.

        """
        if isinstance(value, self._terms_type):
            setattr(value, '_termsum', self)
            self.terms.append(value)
            setattr(self, value.name, value)
        elif isinstance(value, self.__class__):
            for term in value.terms:
                setattr(term, '_termsum', self)
                self.terms.append(term)
                setattr(self, term.name, term)
        else:
            msg = (f'Cannot add type(value)={value} to {self.__class__}.')
            raise TypeError(msg)

    def __iadd__(self, other):
        """Overloaded += operation.

        This method is called when `other` is added to `self`.

        Parameters
        ----------
        other : micromagneticmodel.util.Term
            A term to be added to `self`.

        Return
        ------
        self
            It return the object itself.

        """
        self._add(other)
        return self

    @property
    def _script(self):
        """This method should be implemented by a specific micromagnetic
        calculator

        """
        raise NotImplementedError

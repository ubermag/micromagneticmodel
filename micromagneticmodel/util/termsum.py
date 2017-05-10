import abc


class TermSum(metaclass=abc.ABCMeta):
    def __init__(self):
        self.terms = []

    @property
    @abc.abstractmethod
    def _lefthandside(self): pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _terms_type(self): pass  # pragma: no cover

    @property
    def _repr(self):
        """Property creating and returning representation string."""
        terms_repr = [term._repr for term in self.terms]
        return " + ".join(terms_repr)

    @property
    def _latex(self):
        s = self._lefthandside

        for term in self.terms:
            if term._latex[1] != "-" and s[-1] != "=":
                s += "+"
            s += term._latex[1:-1]

        if self.terms == []:
            s += "0"
        s += "$"

        return s

    def __repr__(self):
        """A representation method."""
        return self._repr

    def _repr_latex_(self):
        """A LaTeX representation method in Jupyter notebook."""
        return self._latex

    def _add(self, value):
        """Add Term or TermSum to the TermSum"""
        if isinstance(value, self._terms_type):
            setattr(value, "_termsum", self)
            self.terms.append(value)
            setattr(self, value.name, value)
        elif isinstance(value, self.__class__):
            for term in value.terms:
                setattr(term, "_termsum", self)
                self.terms.append(term)
                setattr(self, term.name, term)
        else:
            msg = ("Cannot add type(value)={} "
                   "to {}.".format(value, self.__class__))
            raise TypeError(msg)

    def __iadd__(self, other):
        """Implementation for += operation."""
        self._add(other)
        return self

    @property
    def _script(self):
        """This method should be provided by the specific micromagnetic
        calculator"""
        raise NotImplementedError

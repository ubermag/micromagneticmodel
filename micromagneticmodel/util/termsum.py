import abc


class TermSum(metaclass=abc.ABCMeta):
    def __init__(self):
        self.terms = []

    def __repr__(self):
        """A representation method."""
        return self._repr_str

    @property
    def _repr_str(self):
        """Property creating and returning representation string."""
        terms_repr = [term._repr_str for term in self.terms]
        return " + ".join(terms_repr)

    def _repr_latex_(self):
        """A LaTeX representation method in Jupyter notebook."""
        return self.latex_str

    @property
    def latex_str(self):
        s = self._lefthandside

        for term in self.terms:
            if term.latex_str[1] != "-" and s[-1] != "=":
                s += "+"
            s += term.latex_str[1:-1]

        if self.terms == []:
            s += "0"
        s += "$"

        return s

    @abc.abstractmethod
    def _lefthandside(self): pass  # pragma: no cover

    @abc.abstractmethod
    def _terms_type(self): pass  # pragma: no cover

    def add(self, value):
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
        self.add(other)
        return self

    @property
    def script(self):
        """This method should be provided by the specific micromagnetic
        calculator"""
        raise NotImplementedError

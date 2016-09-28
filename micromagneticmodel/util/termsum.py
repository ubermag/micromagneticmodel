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
    def add(self, value): pass  # pragma: no cover

    def __iadd__(self, other):
        """Implementation for += operation."""
        self.add(other)
        return self

    def __getattr__(self, name):
        for term in self.terms:
            if term.name == name:
                return term
        raise AttributeError("Term does not exist.")

    def script(self):
        """This method should be provided by the specific micromagnetic
        calculator"""
        raise NotImplementedError

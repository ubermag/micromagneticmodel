import six
import abc


@six.add_metaclass(abc.ABCMeta)
class Term(object):
    @abc.abstractmethod
    def __init__(self): pass

    @abc.abstractmethod
    def _repr_str(self): pass

    @abc.abstractmethod
    def __add__(self, other): pass

    def __repr__(self):
        """A representation method."""
        return self._repr_str

    def _repr_latex_(self):
        """A LaTeX representation method in Jupyter notebook."""
        return self.latex_str

    def __radd__(self, other):
        """Reverse addition for creating a list of energy objects."""
        other.add(self)
        return other

    def script(self):
        """This method should be provided by the specific micromagnetic
        calculator"""
        raise NotImplementedError

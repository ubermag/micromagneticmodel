import abc
import importlib


class Term(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self): pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _repr(self): pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _latex(self): pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _termsum_type(self): pass  # pragma: no cover

    def __repr__(self):
        """A representation method."""
        return self._repr

    def _repr_latex_(self):
        """A LaTeX representation method in Jupyter notebook."""
        return self._latex

    def __add__(self, other):
        """Addition operation."""
        module = importlib.__import__(self.__class__.__module__)
        termsum = getattr(module, self._termsum_type)()
        termsum._add(self)
        termsum._add(other)
        return termsum

    def __radd__(self, other):
        """Reverse addition for creating a list of energy objects."""
        other._add(self)
        return other

    @property
    def _script(self):
        """This method should be provided by the specific micromagnetic
        calculator"""
        raise NotImplementedError

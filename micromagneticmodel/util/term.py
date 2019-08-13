import abc
import importlib


class Term(metaclass=abc.ABCMeta):
    """An abstract class for the implementation of individual terms.

    This class should be inherited by a class which implements a
    particular energy or dynamics term.

    """
    @abc.abstractmethod
    def __init__(self):
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _repr(self):
        """Representation string returned by `__repr__` method.

        This should be implemented in a derived class. It can be
        implemented as a global class attribute - it does not have to
        be a property.

        """
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _latex(self):
        """Representation string returned by `_repr_latex` method inside
        Jupyter notebook.

        This should be implemented in a derived class. It can be
        implemented as a global class attribute - it does not have to
        be a property.

        """
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def _termsum_type(self):
        """A class which is a result of term addition.

        This should be implemented in a derived class. It can be
        implemented as a global class attribute - it does not have to
        be a property. It is the type of a class obtained when two
        terms are added. For instance, the term sum of two energy
        terms is `micromagneticmodel.Hamiltonian`.

        """
        pass  # pragma: no cover

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

    def __add__(self, other):
        """Overloaded addition operation.

        This method is called when two terms are added together.

        Parameters
        ----------
        other : micromagneticmodel.util.Term
            A term which should be added to `self`.

        Return
        ------
        self._term_type
            A term sum class. For instance, the term sum of two energy
            terms is `micromagneticmodel.Hamiltonian`.

        """
        module = importlib.__import__(self.__class__.__module__)
        termsum = getattr(module, self._termsum_type)()
        termsum._add(self)
        termsum._add(other)
        return termsum

    def __radd__(self, other):
        """Overloaded += operation.

        This method is called when `self` is added to `other`.

        Parameters
        ----------
        other : micromagneticmodel.util.TermSum
            A term sum to which `self` should be added.

        Return
        ------
        self._term_type
            A term sum class. For instance, the term sum of two energy
            terms is `micromagneticmodel.Hamiltonian`.

        """
        other._add(self)
        return other

    @property
    def _script(self):
        """This method should be implemented by a specific micromagnetic
        calculator

        """
        raise NotImplementedError

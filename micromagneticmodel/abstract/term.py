import abc

import micromagneticmodel as mm

from .abstract import Abstract


class Term(Abstract):
    """Abstract class for deriving energy and dynamics terms.

    This class is derived from ``micromagneticmodel.abstract.Abstract``.

    """

    @property
    @abc.abstractmethod
    def _container_class(self):
        """A class of a container, which is the result of adding terms."""
        pass  # pragma: no cover

    def __eq__(self, other):
        """Relational operator ``==``.

        Two terms are considered to be equal if they are instances of the same
        class.

        Parameters
        ----------
        other : micromagneticmodel.Term

            Second operand.

        Returns
        -------
        bool

            ``True`` if two terms are instances of the same class and ``False``
            otherwise.

        Examples
        --------
        1. Comparing terms.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> zeeman = mm.Zeeman(H=(0, 0, 1e6))
        >>> damping = mm.Damping(alpha=0.1)
        >>> demag = mm.Demag()
        ...
        >>> exchange == exchange
        True
        >>> exchange == mm.Exchange(A=5e-11)  # only class is checked
        True
        >>> zeeman != exchange
        True
        >>> zeeman == exchange
        False
        >>> damping == damping
        True
        >>> damping != exchange
        True
        >>> demag == exchange
        False

        """
        if isinstance(other, self.__class__):
            return True
        else:
            return False

    def __add__(self, other):
        """Binary ``+`` operator.

        It can be applied only between two ``micromagneticmodel.abstract.Term``
        objects.

        Parameters
        ----------
        other : micromagneticmodel.abstract.Term

            Second operand.

        Returns
        -------
        micromagneticmodel.abstract.Container

            Resulting sum.

        Examples
        --------
        1. Adding energy terms.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> demag = mm.Demag()
        ...
        >>> container = exchange + demag
        >>> type(container)
        <class 'micromagneticmodel.energy.energy.Energy'>

        2. Adding dynamics terms.

        >>> precession = mm.Precession(gamma0=mm.consts.gamma0)
        >>> damping = mm.Damping(alpha=0.01)
        ...
        >>> container = precession + damping
        >>> type(container)
        <class 'micromagneticmodel.dynamics.dynamics.Dynamics'>

        """
        result = getattr(mm, self._container_class)()
        result += self
        result += other
        return result

    @property
    @abc.abstractmethod
    def _reprlatex(self):
        """ "LaTeX representation abstract method, rendered inside Jupyter and
        returned by ``micromagneticmodel.Term._repr_latex_``.

        """
        pass  # pragma: no cover

    def _repr_latex_(self):
        """ "LaTeX representation method, rendered in Jupyter. This method has
        the priority over ``__repr__`` in Jupyter.

        Returns
        -------
        str

            LaTeX representation string.

        Examples
        --------
        1. Getting LaTeX representation string.

        >>> import micromagneticmodel as mm
        ...
        >>> zeeman = mm.Zeeman(H=(100, 0, 0))
        >>> zeeman._repr_latex_()
        '$-\\\\mu_{0}M_\\\\text{s} \\\\mathbf{m} \\\\cdot \\\\mathbf{H}$'
        >>> # zeeman  # inside Jupyter

        """
        return f"${self._reprlatex}$"

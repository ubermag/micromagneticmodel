import abc

import ubermagutil as uu

import micromagneticmodel as mm


@uu.inherit_docs
class DynamicsTerm(mm.abstract.Term):
    """A parent class for all dynamics terms."""

    _container_class = "Dynamics"

    @abc.abstractmethod
    def dmdt(self, m, Heff):
        pass  # pragma: no cover

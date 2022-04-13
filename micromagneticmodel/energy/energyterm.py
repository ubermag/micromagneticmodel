import abc

import ubermagutil as uu

import micromagneticmodel as mm


@uu.inherit_docs
class EnergyTerm(mm.abstract.Term):
    """A parent class for all energy terms."""

    _container_class = "Energy"

    def energy(self, m):
        raise NotImplementedError  # can be implemented as (Heff*m).integrate

    def density(self, m):
        raise NotImplementedError  # can be implemented as Heff*m

    @abc.abstractmethod
    def effective_field(self, m):
        pass  # pragma: no cover

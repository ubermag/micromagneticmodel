import abc
import micromagneticmodel as mm


class EnergyTerm(mm.util.Term):
    """A parent class for all energy terms.

    """
    _termscontainer_class = 'Energy'

    def energy(self, m):
        raise NotImplementedError  # can be implemented as Heff*m.integrate

    def density(self, m):
        raise NotImplementedError  # can be implemented as Heff*m

    @abc.abstractmethod
    def effective_field(self, m):
        pass

import abc
import micromagneticmodel as mm


class EnergyTerm(mm.util.Term):
    """A parent class for all energy terms.

    """
    _termsum_class = 'Energy'

    @abc.abstractmethod
    def energy(self, m):
        pass

    @abc.abstractmethod
    def density(self, m):
        pass

    @abc.abstractmethod
    def effective_field(self, m):
        pass

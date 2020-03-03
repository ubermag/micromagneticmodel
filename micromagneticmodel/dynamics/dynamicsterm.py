import abc
import ubermagutil as uu
import micromagneticmodel as mm


@uu.inherit_docs
class DynamicsTerm(mm.util.Term):
    """A parent class for all dynamics terms.

    """
    _container_class = 'Dynamics'

    @abc.abstractmethod
    def dmdt(self, m, Heff):
        raise NotImplementedError

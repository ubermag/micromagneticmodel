import abc
import ubermagutil as uu
from ..util import Term


@uu.inherit_docs
class DynamicsTerm(Term):
    """A parent class for all dynamics terms.

    """
    _container_class = 'Dynamics'

    @abc.abstractmethod
    def dmdt(self, m, Heff):
        pass

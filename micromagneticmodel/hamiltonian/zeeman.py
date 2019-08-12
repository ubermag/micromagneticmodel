import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(H=ts.Vector(size=3),
               name=ts.Name(const=True))
class Zeeman(EnergyTerm):
    _latex = r'$-\mu_{0}M_\text{s} \mathbf{m} \cdot \mathbf{H}$'

    def __init__(self, H, name='zeeman'):
        """A Zeeman energy class.

        This method internally calls set_H method. Refer to its documentation.

        """
        self.H = H
        self.name = name

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return 'Zeeman(H={}, name=\'{}\')'.format(self.H, self.name)

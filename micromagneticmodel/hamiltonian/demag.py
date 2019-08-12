import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(name=ts.Name(const=True))
class Demag(EnergyTerm):
    _latex = (r'$-\frac{1}{2}\mu_{0}M_\text{s}'
              r'\mathbf{m} \cdot \mathbf{H}_\text{d}$')

    def __init__(self, name='demag'):
        """Abstract demagnetisation energy class."""
        self.name = name

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return 'Demag(name=\'{}\')'.format(self.name)

from micromagneticmodel.hamiltonian import EnergyTerm
from micromagneticmodel.util.typesystem import UnsignedReal, String, typesystem


@typesystem(name=String,
            latex_str=String)
class Demag(EnergyTerm):
    def __init__(self, name='demag'):
        """Abstract demagnetisation energy class."""
        self.name = name
        self.latex_str = ('$-\\frac{1}{2}\mu_{0}M_\\text{s}'
                          '\mathbf{m} \cdot \mathbf{H}_\\text{d}$')

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return 'Demag()'

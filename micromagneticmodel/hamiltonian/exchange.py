import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(A=ts.Scalar(unsigned=True),
               name=ts.Name(const=True))
class Exchange(EnergyTerm):
    _latex = r'$A (\nabla \mathbf{m})^{2}$'

    def __init__(self, A, name="exchange"):
        """An exchange energy class.

        Args:
            A (Real): exchange energy constant (J/m)

        """
        self.A = A
        self.name = name

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return 'Exchange(A={}, name=\'{}\')'.format(self.A, self.name)

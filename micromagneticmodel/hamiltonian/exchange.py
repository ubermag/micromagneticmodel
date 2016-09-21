import micromagneticmodel.util.typesystem as ts
from micromagneticmodel.hamiltonian import EnergyTerm


@ts.typesystem(A=ts.UnsignedReal,
               name=ts.String,
               latex_str=ts.String)
class Exchange(EnergyTerm):
    def __init__(self, A, name='exchange'):
        """An exchange energy class.

        Args:
            A (Real): exchange energy constant (J/m)

        """
        self.A = A
        self.name = name
        self.latex_str = ('$A [(\\nabla m_{x})^{2} + '
                          '(\\nabla m_{y})^{2} + '
                          '(\\nabla m_{z})^{2}]$')

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return 'Exchange(A={})'.format(self.A)

from numbers import Real
from energyterm import EnergyTerm


class ExchangeAbstract(EnergyTerm):
    latex_str = ("$A [(\\nabla m_{x})^{2} + "
                 "(\\nabla m_{y})^{2} + "
                 "(\\nabla m_{z})^{2}]$")
    
    def __init__(self, A):
        """An exchange energy class.

        Args:
            A (Real): exchange energy constant (J/m)

        """
        if not isinstance(A, Real) or A <= 0:
            raise ValueError('A must be a positive real number.')
        self.A = A

    

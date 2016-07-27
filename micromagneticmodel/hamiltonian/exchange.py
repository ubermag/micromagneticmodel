from numbers import Real
from micromagneticmodel.hamiltonian import EnergyTerm


class Exchange(EnergyTerm):
    _name = "exchange"
    _latex_str = ("$A [(\\nabla m_{x})^{2} + "
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

    @property
    def _repr_str(self):
        """A representation string property.
        
        Returns:
           A representation string.

        """
        return "Exchange(A={})".format(self.A)

    def script(self):
        """This method should be provided by the specific micromagnetic
        calculator"""
        raise NotImplementedError

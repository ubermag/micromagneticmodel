from numbers import Real
from micromagneticmodel.hamiltonian import EnergyTerm


class ExchangeAbstract(EnergyTerm):
    _name = 'exchange'
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

    def __repr__(self):
        return "Exchange(A={})".format(self.A)

    def calculator_script(self):
        """This needs to be provided by the specific micromagnetic
        calculator"""
        raise NotImplementedError()

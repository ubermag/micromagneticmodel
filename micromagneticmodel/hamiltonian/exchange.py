import joommfutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(A=ts.UnsignedReal,
               name=ts.ObjectName)
class Exchange(EnergyTerm):
    latex_str = ("$A [(\\nabla m_{x})^{2} + "
                 "(\\nabla m_{y})^{2} + "
                 "(\\nabla m_{z})^{2}]$")

    def __init__(self, A, name="exchange"):
        """An exchange energy class.

        Args:
            A (Real): exchange energy constant (J/m)

        """
        self.A = A
        self.name = name

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "Exchange(A={})".format(self.A)

import joommfutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(D=ts.Real,
               name=ts.ConstantObjectName)
class DMI(EnergyTerm):
    def __init__(self, D, kind="bulk", name="dmi"):
        """A DMI energy class.

        Args:
            D (Real): DMI energy constant (J/m**2)

        """
        self.D = D
        self.name = name
        self.kind = kind

    @property
    def _latex(self):
        if self.kind == "bulk":
            return ("$D \mathbf{m} \\cdot (\\nabla \\times \mathbf{m})$")
        elif self.kind == "interfacial":
            return ("$D \\left[ \\left( m_{x} \\frac{ \\partial m_{z}}{\\partial x} "
                    "- m_{z}\\frac{\\partial m_{x}}{\\partial x} \\right)"
                    "+ \\left( m_{y}\\frac{\partial m_{z}}{\\partial y}"
                    "- m_{z}\\frac{\\partial m_{y}}{\\partial y} \\right)\\right]$")

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return ("DMI(D={}, kind=\"{}\", "
                "name=\"{}\")").format(self.D, self.kind, self.name)

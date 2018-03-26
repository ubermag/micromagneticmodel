import joommfutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(D=ts.Real,
               name=ts.ConstantObjectName)
class DMI(EnergyTerm):
    def __init__(self, D, crystalclass="t", name="dmi"):
        """A DMI energy class.

        Args:
            D (Real): DMI energy constant (J/m**2)

        """
        self.D = D
        self.crystalclass = crystalclass.lower()
        self.name = name

    @property
    def _latex(self):
        if self.crystalclass == "t" or self.crystalclass == "o":
            return ("$D \mathbf{m} \\cdot (\\nabla \\times \mathbf{m})$")
        elif self.crystalclass == "cnv":
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
        return ("DMI(D={}, crystalclass=\"{}\", "
                "name=\"{}\")").format(self.D, self.crystalclass, self.name)

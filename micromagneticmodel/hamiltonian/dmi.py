import joommfutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(D=ts.Real,
               crystalclass=ts.FromSet(allowed_values={"cnv", "t",
                                                       "o", "d2d",
                                                       "interfacial"}),
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
        if self.crystalclass in ["t", "o"]:
            return ("$D \mathbf{m} \\cdot (\\nabla \\times \mathbf{m})$")
        elif self.crystalclass in ["cnv", "interfacial"]:
            return ("$D ( \mathbf{m} \\cdot \\nabla m_{z} "
                    "- m_{z} \\nabla \\cdot \mathbf{m} )$")
        else:
            return ("$D\mathbf{m} \\cdot \\left( \\frac{\\partial "
                    "\mathbf{m}}{\\partial x} \\times \hat{x} - "
                    "\\frac{\\partial \mathbf{m}}{\\partial y} "
                    "\\times \hat{y} \\right)$")

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return ("DMI(D={}, crystalclass=\"{}\", "
                "name=\"{}\")").format(self.D, self.crystalclass, self.name)

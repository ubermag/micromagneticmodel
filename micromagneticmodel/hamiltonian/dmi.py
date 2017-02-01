import joommfutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(D=ts.Real,
               name=ts.ObjectName)
class DMI(EnergyTerm):
    _latex = ("$D \mathbf{m} \\cdot (\\nabla \\times \mathbf{m})$")

    def __init__(self, D, name="dmi"):
        """A DMI energy class.

        Args:
            D (Real): DMI energy constant (J/m**2)

        """
        self.D = D
        self.name = name

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "DMI(D={})".format(self.D)

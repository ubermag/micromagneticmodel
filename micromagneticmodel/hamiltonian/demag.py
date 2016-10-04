import joommfutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(name=ts.ObjectName)
class Demag(EnergyTerm):
    latex_str = ("$-\\frac{1}{2}\mu_{0}M_\\text{s}"
                 "\mathbf{m} \cdot \mathbf{H}_\\text{d}$")

    def __init__(self, name="demag"):
        """Abstract demagnetisation energy class."""
        self.name = name

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "Demag()"

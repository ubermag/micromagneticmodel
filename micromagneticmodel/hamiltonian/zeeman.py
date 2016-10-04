import joommfutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(H=ts.RealVector(size=3),
               name=ts.ObjectName)
class Zeeman(EnergyTerm):
    latex_str = "$-\mu_{0}M_\\text{s} \mathbf{m} \cdot \mathbf{H}$"

    def __init__(self, H, name="zeeman"):
        """A Zeeman energy class.

        This method internally calls set_H method. Refer to its documentation.

        """
        self.H = H
        self.name = name

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "Zeeman(H={})".format(self.H)

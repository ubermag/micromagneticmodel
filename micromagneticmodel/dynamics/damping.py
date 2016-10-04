import joommfutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(alpha=ts.UnsignedReal,
               name=ts.ObjectName)
class Damping(DynamicsTerm):
    latex_str = ("$\\alpha \mathbf{m} \\times"
                 "\\frac{\partial \mathbf{m}}{\partial t}$")

    def __init__(self, alpha, name="damping"):
        """A damping dynamics term class.

        Args:
            alpha (Real): Gilbert damping

        """
        self.alpha = alpha
        self.name = name

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "Damping(alpha={})".format(self.alpha)

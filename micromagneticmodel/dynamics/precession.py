import joommfutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(gamma=ts.UnsignedReal,
               name=ts.ObjectName)
class Precession(DynamicsTerm):
    latex_str = ("$-\gamma \mathbf{m} \\times "
                 "\mathbf{H}_\\text{eff}$")

    def __init__(self, gamma, name="precession"):
        """A precession dynamics term class.

        Args:
            gamma (Real): gyrotropic ratio (m/As)

        """
        self.gamma = gamma
        self.name = name

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "Precession(gamma={})".format(self.gamma)

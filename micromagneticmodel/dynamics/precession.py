import joommfutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(gamma=ts.UnsignedReal,
               name=ts.ConstantObjectName)
class Precession(DynamicsTerm):
    _latex = ("$-\gamma_{0}^{*} \mathbf{m} \\times "
              "\mathbf{H}_\\text{eff}$")

    def __init__(self, gamma, name="precession"):
        """A precession dynamics term class.

        Args:
            gamma (Real): gyrotropic ratio (m/As)

        """
        self.gamma = gamma
        self.name = name

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "Precession(gamma={}, name=\"{}\")".format(self.gamma, self.name)

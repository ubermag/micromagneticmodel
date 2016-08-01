from micromagneticmodel.dynamics import DynamicsTerm
from micromagneticmodel.util.typesystem import UnsignedReal, String, typesystem


@typesystem(gamma=UnsignedReal,
            name=String)
class Precession(DynamicsTerm):
    def __init__(self, gamma, name='precession'):
        """A precession dynamics term class.

        Args:
            gamma (Real): gyrotropic ratio (m/As)

        """
        self.gamma = gamma
        self.name = name
        self.latex_str = ('$-\gamma \mathbf{m} \\times '
                          '\mathbf{H}_\\text{eff}$')

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return 'Precession(gamma={})'.format(self.gamma)

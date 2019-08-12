import ubermagutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(gamma=ts.Scalar(unsigned=True),
               name=ts.Name(const=True))
class Precession(DynamicsTerm):
    _latex = (r'$-\gamma_{0}^{*} \mathbf{m} \times '
              r'\mathbf{H}_\text{eff}$')

    def __init__(self, gamma, name='precession'):
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
        return 'Precession(gamma={}, name=\'{}\')'.format(self.gamma, self.name)

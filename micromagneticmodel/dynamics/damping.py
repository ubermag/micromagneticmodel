import ubermagutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(alpha=ts.Scalar(unsigned=True),
               name=ts.Name(const=True))
class Damping(DynamicsTerm):
    _latex = (r'$\alpha \mathbf{m} \times'
              r'\frac{\partial \mathbf{m}}{\partial t}$')

    def __init__(self, alpha, name='damping'):
        """A damping dynamics term class.

        Args:
            alpha (Real): Gilbert damping

        """
        self.alpha = alpha
        self.name = name

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return 'Damping(alpha={}, name=\'{}\')'.format(self.alpha, self.name)

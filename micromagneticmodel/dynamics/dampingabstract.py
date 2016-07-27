from numbers import Real
from micromagneticmodel.dynamics import DynamicsTerm


class DampingAbstract(DynamicsTerm):
    _name = 'damping'
    _latex_str = ("$\\alpha \mathbf{m} \\times"
                  "\\frac{\partial \mathbf{m}}{\partial t}$")

    def __init__(self, alpha):
        """A damping dynamics term class.

        Args:
            alpha (Real): Gilbert damping

        """
        if not isinstance(alpha, Real) or alpha <= 0:
            raise ValueError('alpha must be a positive real number.')
        self.alpha = alpha

    @property
    def _repr_str(self):
        """A representation string property.
        
        Returns:
           A representation string.

        """
        return "Damping(alpha={})".format(self.alpha)

from numbers import Real
from micromagneticmodel.dynamics import DynamicsTerm


class PrecessionAbstract(DynamicsTerm):
    _name = "precession"
    _latex_str = ("$-\gamma \mathbf{m} \\times \mathbf{H}_\\text{eff}$")
    
    def __init__(self, gamma):
        """A precession dynamics term class.

        Args:
            gamma (Real): gyrotropic ratio (m/As)

        """
        if not isinstance(gamma, Real) or gamma <= 0:
            raise ValueError("gamma must be a positive real number.")
        self.gamma = gamma

    @property
    def _repr_str(self):
        """A representation string property.
        
        Returns:
           A representation string.

        """
        return "Precession(gamma={})".format(self.gamma)

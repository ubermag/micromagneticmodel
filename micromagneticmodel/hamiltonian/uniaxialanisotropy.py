import joommfutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(K=ts.Real,
               u=ts.RealVector(size=3),
               name=ts.ObjectName)
class UniaxialAnisotropy(EnergyTerm):
    latex_str = "$K (\mathbf{m} \cdot \mathbf{u})^{2}$"

    def __init__(self, K, u, name="uniaxialanisotropy"):
        """A uniaxial anisotropy energy abstract class.

        Args:
            K (Real): Uniaxial anisotropy energy constant (J/m**3)
            u (tuple, list, np.ndarray): Easy axis

        """
        self.K = K
        self.u = u
        self.name = name

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "UniaxialAnisotropy(K={}, u={})".format(self.K, self.u)

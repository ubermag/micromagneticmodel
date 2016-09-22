from micromagneticmodel.hamiltonian import EnergyTerm
from micromagneticmodel.util.typesystem import Real, String, \
    RealVector3D, typesystem


@typesystem(K=Real,
            u=RealVector3D,
            name=String)
class UniaxialAnisotropy(EnergyTerm):
    latex_str = '$K (\mathbf{m} \cdot \mathbf{u})^{2}$'

    def __init__(self, K, u, name='uniaxialanisotropy'):
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
        return 'UniaxialAnisotropy(K={}, u={})'.format(self.K, self.u)

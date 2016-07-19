import numpy as np
from numbers import Real
from micromagneticmodel.hamiltonian import EnergyTerm


class UniaxialAnisotropyAbstract(EnergyTerm):
    _name = 'uniaxialanisotropy'
    _latex_str = '$K (\mathbf{m} \cdot \mathbf{u})^{2}$'

    def __init__(self, K, u):
        """A uniaxial anisotropy energy abstract class.

        Args:
            K (Real): Uniaxial anisotropy energy constant (J/m**3)
            u (tuple, list, np.ndarray): Easy axis

        """
        if not isinstance(K, Real):
            raise ValueError('K must be a positive real number.')
        if not isinstance(u, (tuple, list, np.ndarray)) or len(u) != 3:
            raise ValueError('u must be a 3-element tuple, '
                             'list, or np.ndarray.')
        if not all([isinstance(i, Real) for i in u]):
            raise ValueError('All elements of u must be real numbers.')
        self.K = K
        self.u = u

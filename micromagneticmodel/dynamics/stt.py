import ubermagutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(u=ts.Vector(size=3),
               beta=ts.Scalar,
               name=ts.Name(const=True))
class STT(DynamicsTerm):
    _latex = (r'$-(\mathbf{u} \cdot \boldsymbol\nabla)\mathbf{m} + '
              r'\beta\mathbf{m} \times \big[(\mathbf{u} \cdot '
              r'\boldsymbol\nabla)\mathbf{m}\big]$')

    def __init__(self, u, beta, name='stt'):
        """A spin transfer torque term.

        Args:
            u (RealVector): velocity vector
            beta (Real): non-adiabatic parameter

        """
        self.u = u
        self.beta = beta
        self.name = name

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return ('STT(u={}, beta={}, '
                'name=\'{}\')').format(self.u, self.beta, self.name)

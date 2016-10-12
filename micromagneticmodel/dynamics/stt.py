import joommfutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(u=ts.RealVector(size=3),
               beta=ts.Real,
               name=ts.ObjectName)
class STT(DynamicsTerm):
    latex_str = ("$-(\mathbf{u} \cdot \\boldsymbol\\nabla)\mathbf{m} + "
                 "\\beta\mathbf{m} \\times \\big[(\mathbf{u} \cdot "
                 "\\boldsymbol\\nabla)\mathbf{m}\\big]$")

    def __init__(self, u, beta, name="stt"):
        """A spin transfer torque term.

        Args:
            u (RealVector): velocity vector
            beta (Real): non-adiabatic parameter

        """
        self.u = u
        self.beta = beta
        self.name = name

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "STT(u={}, beta={})".format(self.u, self.beta)

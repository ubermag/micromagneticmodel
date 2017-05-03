import joommfutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(K1=ts.Real,
               K2=ts.Real,
               u=ts.RealVector(size=3),
               name=ts.ObjectName)
class UniaxialAnisotropy(EnergyTerm):
    def __init__(self, K1, u, K2=0, name="uniaxialanisotropy"):
        """Uniaxial anisotropy energy abstract class.

        Parameters
        ----------
            K1, K2 : Real
                Uniaxial anisotropy energy constant (J/m**3)
            u : (3,) array_like
                uniaxial anisotropy axis

        """
        self.K1 = K1
        self.K2 = K2
        self.u = u
        self.name = name

    @property
    def _latex(self):
        first_term = "$-K_{1} (\mathbf{m} \cdot \mathbf{u})^{2}$"
        second_term = "$-K_{2} (\mathbf{m} \cdot \mathbf{u})^{4}$"
        if self.K2 == 0:
            return first_term
        else:
            return first_term + second_term

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "UniaxialAnisotropy(K1={}, K2={}, u={})".format(self.K1,
                                                               self.K2,
                                                               self.u)

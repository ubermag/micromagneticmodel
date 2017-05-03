import joommfutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(K1=ts.Real,
               K2=ts.Real,
               u=ts.RealVector(size=3),
               name=ts.ConstantObjectName)
class UniaxialAnisotropy(EnergyTerm):
    def __init__(self, K1, u, K2=0, name="uniaxialanisotropy"):
        """Uniaxial anisotropy energy abstract class.

        Parameters
        ----------
        K1, K2 : Real
            Uniaxial anisotropy energy constant (J/m**3)
        u : (3,) array_like
            Uniaxial anisotropy axis

        Examples
        --------
        Creating a uniaxial anisotropy object

        >>> import micromagneticmodel as mm
        >>> ua = mm.UniaxialAnisotropy(K1=5e6, K2=1e3, u=(0, 0, 1))

        """
        self.K1 = K1
        self.K2 = K2
        self.u = u
        self.name = name

    @property
    def _latex(self):
        first_term = "-K_{1} (\mathbf{m} \cdot \mathbf{u})^{2}"
        second_term = "-K_{2} (\mathbf{m} \cdot \mathbf{u})^{4}"
        if self.K2 == 0:
            return "${}$".format(first_term)
        else:
            return "${}$".format(first_term+second_term)

    @property
    def _repr(self):
        """A representation string property.

        Returns
        -------
        str
            A representation string.

        """
        return ("UniaxialAnisotropy(K1={}, K2={}, u={}, "
                "name=\"{}\")").format(self.K1, self.K2, self.u, self.name)

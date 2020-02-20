import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(K1=ts.Parameter(descriptor=ts.Scalar(),
                               otherwise=df.Field),
               u=ts.Parameter(descriptor=ts.Vector(size=3),
                              otherwise=df.Field),
               name=ts.Name(const=True))
class UniaxialAnisotropy(EnergyTerm):
    def __init__(self, K1, u, name='uniaxialanisotropy',
                 **kwargs):
        """Uniaxial anisotropy energy term.

        This object models aniaxial anisotropy energy term. It takes
        the anisotropy energy constant `K1` and the anisotropy axis
        `u`. `name` can also be passed as input parameter. In
        addition, any further parameters, required by a specific
        micromagnetic calculator can be passed.

        Parameters
        ----------
        K1, : int, float, dict, discretisedfield.Field
            A single positive value (int, float) can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `K1={'region1': 1e-12,
            'region2': 5e-12}`. If it is possible to define the
            parameter "per cell", `discretisedfield.Field` can be
            passed.
        u : array_like, dict, discretisedfield.Field
            A length-3 array_like (tuple, list, `numpy.ndarray`),
            which consists of `numbers.Real` can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `H={'region1': (0, 0, 1),
            'region2': (1, 0, 0)}`. If it is possible to define the
            parameter "per cell", `discretisedfield.Field` can be
            passed.
        name : str
            Name of the energy term.

        Examples
        --------
        1. Initialising the uniaxial anisotropy energy term.

        >>> import micromagneticmodel as mm
        >>> import discretisedfield as df
        ...
        >>> ua1 = mm.UniaxialAnisotropy(K1=1e6, u=(0, 0, 1))
        >>> ua2 = mm.UniaxialAnisotropy(K1={'r1': 1e6, 'r2': 2e6},
        ...                             u=(0, 0, 1))
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
        ...                cell=(1e-9, 1e-9, 1e-9))
        >>> field = df.Field(mesh, dim=1, value=3e6)
        >>> ua3 = mm.UniaxialAnisotropy(K1=field, u=(0, 0, 1))

        """
        self.K1 = K1
        self.u = u
        self.name = name
        self.__dict__.update(kwargs)

    @property
    def _latex(self):
        return r'$-K_{1} (\mathbf{m} \cdot \mathbf{u})^{2}$'

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return (f'UniaxialAnisotropy(K1={self.K1}, '
                f'u={self.u}, name=\'{self.name}\')')

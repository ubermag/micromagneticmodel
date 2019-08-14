import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(K1=ts.Parameter(descriptor=ts.Scalar(),
                               otherwise=df.Field),
               K2=ts.Parameter(descriptor=ts.Scalar(),
                               otherwise=df.Field),
               u=ts.Parameter(descriptor=ts.Vector(size=3),
                              otherwise=df.Field),
               name=ts.Name(const=True))
class UniaxialAnisotropy(EnergyTerm):
    def __init__(self, K1, u, K2=0, name='uniaxialanisotropy',
                 **kwargs):
        """Uniaxial anisotropy energy term.

        This object models aniaxial anisotropy energy term. It takes
        the anisotropy energy constants `K1` and optionally `K2`. In
        addition, the anisotropy axis `u` must be provided. `name` can
        also be passed as input parameter. In addition, any further
        parameters, required by a specific micromagnetic calculator
        can be passed.

        Parameters
        ----------
        K1, K2 : int, float, dict, discretisedfield.Field
            A single positive value (int, float) can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `A={'region1': 1e-12,
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
        >>> ua1 = mm.UniaxialAnisotropy(K1=1e6, K2=1e3, u=(0, 0, 1))
        >>> ua2 = mm.UniaxialAnisotropy(K1={'r1': 1e6, 'r2': 2e6},
        ...                             u=(0, 0, 1))
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
        ...                cell=(1e-9, 1e-9, 1e-9))
        >>> field = df.Field(mesh, dim=1, value=3e6)
        >>> ua3 = mm.UniaxialAnisotropy(K1=field, u=(0, 0, 1))

        """
        self.K1 = K1
        self.K2 = K2
        self.u = u
        self.name = name
        self.__dict__.update(kwargs)

    @property
    def _latex(self):
        first_term = r'-K_{1} (\mathbf{m} \cdot \mathbf{u})^{2}'
        second_term = r'-K_{2} (\mathbf{m} \cdot \mathbf{u})^{4}'
        if self.K2 == 0:
            return f'${first_term}$'
        else:
            return f'${first_term+second_term}$'

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return (f'UniaxialAnisotropy(K1={self.K1}, K2={self.K2}, '
                f'u={self.u}, name=\'{self.name}\')')

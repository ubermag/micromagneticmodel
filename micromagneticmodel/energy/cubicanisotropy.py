import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(K1=ts.Parameter(descriptor=ts.Scalar(),
                               otherwise=df.Field),
               u1=ts.Parameter(descriptor=ts.Vector(size=3),
                               otherwise=df.Field),
               u2=ts.Parameter(descriptor=ts.Vector(size=3),
                               otherwise=df.Field),
               name=ts.Name(const=True))
class CubicAnisotropy(EnergyTerm):
    def __init__(self, K1, u1, u2, name='cubicanisotropy',
                 **kwargs):
        """Cubic anisotropy energy term.

        This object models cubic anisotropy energy term. It takes the
        anisotropy energy constant `K1`. In addition, the anisotropy
        axes `u1` and `u2` must be provided. `name` can also be passed
        as input parameter. In addition, any further parameters,
        required by a specific micromagnetic calculator can be passed.

        Parameters
        ----------
        K1 : int, float, dict, discretisedfield.Field
            A single positive value (int, float) can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `A={'region1': 1e-12,
            'region2': 5e-12}`. If it is possible to define the
            parameter "per cell", `discretisedfield.Field` can be
            passed.
        u1, u2 : array_like, dict, discretisedfield.Field
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
        1. Initialising the cubic anisotropy energy term.

        >>> import micromagneticmodel as mm
        >>> import discretisedfield as df
        ...
        >>> ca1 = mm.CubicAnisotropy(K1=1e6, u1=(1, 0, 0),
        ...                          u2=(0, 0, 1))
        >>> ca2 = mm.CubicAnisotropy(K1={'r1': 1e6, 'r2': 2e6},
        ...                          u1=(0, 0, 1), u2=(0, 1, 0))
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
        ...                cell=(1e-9, 1e-9, 1e-9))
        >>> field = df.Field(mesh, dim=1, value=3e6)
        >>> ca3 = mm.CubicAnisotropy(K1=field, u1=(0, 0, 1),
        ...                          u2=(0, 1, 0))

        """
        self.K1 = K1
        self.u1 = u1
        self.u2 = u2
        self.name = name
        self.__dict__.update(kwargs)

    @property
    def _latex(self):
        a1 = r'(\mathbf{m} \cdot \mathbf{u}_{1})^{2}'
        a2 = r'(\mathbf{m} \cdot \mathbf{u}_{2})^{2}'
        a3 = r'(\mathbf{m} \cdot \mathbf{u}_{3})^{2}'
        return r'$-K_{{1}} [{0}{1}+{1}{2}+{2}{0}]$'.format(a1, a2, a3)

    @property
    def _repr(self):
        """A representation string property.

        Returns
        -------
        str
            A representation string.

        """
        return (f'CubicAnisotropy(K1={self.K1}, u1={self.u1}, '
                f'u2={self.u2}, name=\'{self.name}\')')

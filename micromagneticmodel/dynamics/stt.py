import discretisedfield as df
import ubermagutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(u=ts.Parameter(descriptor=ts.Vector(size=3),
                              otherwise=df.Field),
               beta=ts.Parameter(descriptor=ts.Scalar(),
                                 otherwise=df.Field),
               name=ts.Name(const=True))
class STT(DynamicsTerm):
    _latex = (r'$-(\mathbf{u} \cdot \boldsymbol\nabla)\mathbf{m} + '
              r'\beta\mathbf{m} \times \big[(\mathbf{u} \cdot '
              r'\boldsymbol\nabla)\mathbf{m}\big]$')

    def __init__(self, u, beta, name='stt', **kwargs):
        """Spin-Transfer Torque (STT) dynamics term.

        This object models micromagnetic STT dynamics term. It takes
        the non-adiabatic constant `beta`, velocity `u`, and `name` as
        input parameters. In addition, any further parameters,
        required by a specific micromagnetic calculator can be passed.

        Parameters
        ----------
        beta : int, float, dict, discretisedfield.Field
            A single positive value (int, float) can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `beta={'region1': 1e-12,
            'region2': 5e-12}`. If it is possible to define the
            parameter "per cell", `discretisedfield.Field` can be
            passed.
        u : array_like, dict, discretisedfield.Field
            A length-3 array_like (tuple, list, `numpy.ndarray`),
            which consists of `numbers.Real` can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `u={'region1': (0, 0, 3e6),
            'region2': (0, 0, -3e6)}`. If it is possible to define the
            parameter "per cell", `discretisedfield.Field` can be
            passed.
        name : str
            Name of the dynamics term.

        Examples
        --------
        1. Initialising the STT dynamics term.

        >>> import micromagneticmodel as mm
        ...
        >>> stt1 = mm.STT(u=(1, 0, 0), beta=0.5)
        >>> stt2 = mm.STT(u=(1, 0, 0), beta={'r1': 1, 'r2': 2})
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
        ...                cell=(1e-9, 1e-9, 1e-9))
        >>> field = df.Field(mesh, dim=1, value=0.1)
        >>> stt3 = mm.STT(u=(1, 0, 0), beta=field)

        """
        self.u = u
        self.beta = beta
        self.name = name
        self.__dict__.update(kwargs)

    @property
    def _repr(self):
        """A representation string property.

        Returns
        -------
        str
            A representation string.

        """
        return (f'STT(u={self.u}, beta={self.beta}, '
                f'name=\'{self.name}\')')

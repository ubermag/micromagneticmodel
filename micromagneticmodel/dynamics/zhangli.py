import discretisedfield as df
import ubermagutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(u=ts.Parameter(descriptor=ts.Scalar(),
                              otherwise=df.Field),
               beta=ts.Scalar(),
               name=ts.Name(const=True))
class ZhangLi(DynamicsTerm):
    _latex = (r'$-(\mathbf{u} \cdot \boldsymbol\nabla)\mathbf{m} + '
              r'\beta\mathbf{m} \times \big[(\mathbf{u} \cdot '
              r'\boldsymbol\nabla)\mathbf{m}\big]$')

    def __init__(self, u, beta, name='stt', **kwargs):
        """Zhang-Li Spin-Transfer Torque (STT) dynamics term.

        This object models micromagnetic Zhang-Li STT dynamics
        term. It takes the non-adiabatic constant `beta`, velocity `u`
        in the x-direction as a scalar, and `name` as input
        parameters. In addition, any further parameters, required by a
        specific micromagnetic calculator can be passed.

        Parameters
        ----------
        beta : numbers.Real
            A single value (int, float) can be passed.
        u : number.Real, dict, discretisedfield.Field
            `numbers.Real` can be passed, or alternatively, if it is
            defined per region, a dictionary is accepted as well,
            e.g. `u={'region1': 3e6, 'region2': 2e6}`. If it is
            possible to define the parameter "per cell",
            `discretisedfield.Field` can be passed.
        name : str
            Name of the dynamics term.

        Examples
        --------
        1. Initialising the Zhang-Li dynamics term.

        >>> import micromagneticmodel as mm
        ...
        >>> stt1 = mm.ZhangLi(u=1e6, beta=0.5)
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
        ...                cell=(1e-9, 1e-9, 1e-9))
        >>> u = df.Field(mesh, dim=1, value=3e6)
        >>> stt2 = mm.ZhangLi(u=u, beta=0.5)

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
        return (f'ZhangLi(u={self.u}, beta={self.beta}, '
                f'name=\'{self.name}\')')

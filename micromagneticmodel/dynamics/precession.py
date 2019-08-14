import discretisedfield as df
import ubermagutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(gamma=ts.Parameter(descriptor=ts.Scalar(unsigned=True),
                                  otherwise=df.Field),
               name=ts.Name(const=True))
class Precession(DynamicsTerm):
    _latex = (r'$-\gamma_{0}^{*} \mathbf{m} \times '
              r'\mathbf{H}_\text{eff}$')

    def __init__(self, gamma, name='precession', **kwargs):
        """Precession dynamics term.

        This object models micromagnetic precession dynamics term. It
        takes the gyrotropic ratio constant `gamma` and `name` as
        input parameters. In addition, any further parameters,
        required by a specific micromagnetic calculator can be passed.

        Parameters
        ----------
        gamma : int, float, dict, discretisedfield.Field
            A single positive value (int, float) can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `gamma={'region1': 1e-12,
            'region2': 5e-12}`. If it is possible to define the
            parameter "per cell", `discretisedfield.Field` can be
            passed.
        name : str
            Name of the dynamics term.

        Examples
        --------
        1. Initialising the precession dynamics term.

        >>> import micromagneticmodel as mm
        ...
        >>> precession1 = mm.Precession(gamma=mm.consts.gamma0)
        >>> precession2 = mm.Precession(gamma={'r1:r2': 1,
        ...                                    'r2': 2})
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
        ...                cell=(1e-9, 1e-9, 1e-9))
        >>> field = df.Field(mesh, dim=1, value=mm.consts.gamma0)
        >>> precession3 = mm.Precession(gamma=field)

        """
        self.gamma = gamma
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
        return f'Precession(gamma={self.gamma}, name=\'{self.name}\')'

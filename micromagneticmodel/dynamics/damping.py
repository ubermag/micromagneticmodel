import discretisedfield as df
import ubermagutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@ts.typesystem(alpha=ts.Parameter(descriptor=ts.Scalar(unsigned=True),
                                  otherwise=df.Field),
               name=ts.Name(const=True))
class Damping(DynamicsTerm):
    _latex = (r'$\alpha \mathbf{m} \times'
              r'\frac{\partial \mathbf{m}}{\partial t}$')

    def __init__(self, alpha, name='damping', **kwargs):
        """Damping dynamics term.

        This object models micromagnetic damping dynamics term. It
        takes the Gilbert damping constant `alpha` and `name` as input
        parameters. In addition, any further parameters, required by a
        specific micromagnetic calculator can be passed.

        Parameters
        ----------
        alpha : int, float, dict, discretisedfield.Field
            A single positive value (int, float) can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `alpha={'region1': 1e-12,
            'region2': 5e-12}`. If it is possible to define the
            parameter "per cell", `discretisedfield.Field` can be
            passed.
        name : str
            Name of the dynamics term.

        Examples
        --------
        1. Initialising the damping dynamics term.

        >>> import micromagneticmodel as mm
        ...
        >>> damping1 = mm.Damping(alpha=0.1)
        >>> damping2 = mm.Damping(alpha={'r1': 1,
        ...                                    'r2': 2})
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
        ...                cell=(1e-9, 1e-9, 1e-9))
        >>> field = df.Field(mesh, dim=1, value=0.1)
        >>> damping3 = mm.Damping(alpha=field)

        """
        self.alpha = alpha
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
        return f'Damping(alpha={self.alpha}, name=\'{self.name}\')'

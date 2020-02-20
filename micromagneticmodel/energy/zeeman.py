import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(H=ts.Parameter(descriptor=ts.Vector(size=3),
                              otherwise=df.Field),
               name=ts.Name(const=True))
class Zeeman(EnergyTerm):
    _latex = r'$-\mu_{0}M_\text{s} \mathbf{m} \cdot \mathbf{H}$'

    def __init__(self, H, name='zeeman', **kwargs):
        """Zeeman energy term.

        This object models Zeeman energy term. It
        takes the external field `H` and `name` as input
        parameters. In addition, any further parameters, required by a
        specific micromagnetic calculator can be passed.

        Parameters
        ----------
        H : array_like, dict, discretisedfield.Field
            A length-3 array_like (tuple, list, `numpy.ndarray`),
            which consists of `numbers.Real` can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `H={'region1': (0, 0, 3e6),
            'region2': (0, 0, -3e6)}`. If it is possible to define the
            parameter "per cell", `discretisedfield.Field` can be
            passed.
        name : str
            Name of the energy term.

        Examples
        --------
        1. Initialising the Zeeman energy term.

        >>> import micromagneticmodel as mm
        >>> import discretisedfield as df
        ...
        >>> zeeman1 = mm.Zeeman(H=(0, 0, 1e6), name='myzeeman')
        >>> zeeman2 = mm.Zeeman(H={'r1': (0, 0, 1e6),
        ...                        'r2': (0, 0, -1e6)})
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
        ...                cell=(1e-9, 1e-9, 1e-9))
        >>> field = df.Field(mesh, dim=3, value=(0, 0, 1e6))
        >>> zeeman3 = mm.Zeeman(H=field)

        """
        self.H = H
        self.name = name
        self.__dict__.update(kwargs)

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return f'Zeeman(H={self.H}, name=\'{self.name}\')'

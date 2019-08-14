import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(A=ts.Parameter(descriptor=ts.Scalar(unsigned=True),
                              otherwise=df.Field),
               name=ts.Name(const=True))
class Exchange(EnergyTerm):
    _latex = r'$A (\nabla \mathbf{m})^{2}$'

    def __init__(self, A, name='exchange', **kwargs):
        """Micromagnetic exchange energy term.

        This object models micromagnetic exchange energy term. It
        takes the exchange energy constant `A` and `name` as input
        parameters. In addition, any further parameters, required by a
        specific micromagnetic calculator can be passed.

        Parameters
        ----------
        A : int, float, dict, discretisedfield.Field
            A single positive value (int, float) can be
            passed. Alternatively, if it is defined per region, a
            dictionary can be passed, e.g. `A={'region1': 1e-12,
            'region2': 5e-12}`. If it is possible to define the
            parameter "per cell", `discretisedfield.Field` can be
            passed.
        name : str
            Name of the energy term.

        Examples
        --------
        1. Initialising the exchange energy term.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange1 = mm.Exchange(A=1e-12)
        >>> exchange2 = mm.Exchange(A={'r1': 1e-12, 'r2': 2e-12})
        >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
        ...                cell=(1e-9, 1e-9, 1e-9))
        >>> field = df.Field(mesh, dim=1, value=1e12)
        >>> exchange3 = mm.Exchange(A=field)

        """
        self.A = A
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
        return f'Exchange(A={self.A}, name=\'{self.name}\')'

import ubermagutil as uu
import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(A=ts.Parameter(descriptor=ts.Scalar(unsigned=True),
                              otherwise=df.Field),
                              name=ts.Name(const=True))
class Exchange(EnergyTerm):
    """Exchange energy term.

    It takes the exchange energy constant ``A`` and ``name`` as input
    parameters.

    Parameters
    ----------
    A : numbers.Real, dict, discretisedfield.Field

        If a single positive value ``numbers.Real`` is passed, spatially
        constant parameter is defined. For a spatially varying parameter, either
        a dictionary, e.g. ``A={'region1': 1e-12, 'region2': 5e-12}`` (if the
        parameter is defined "per region") or ``discretisedfield.Field`` is
        passed.

    name : str, optional

        Name. Defaults to ``'exchange'``.

    Example
    -------
    1. Defining the exchange energy term.

    >>> import micromagneticmodel as mm
    ...
    >>> exchange1 = mm.Exchange(A=1e-12)
    >>> exchange2 = mm.Exchange(A={'r1': 1e-12, 'r2': 2e-12})
    >>> mesh = df.Mesh(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9),
    ...                cell=(1e-9, 1e-9, 1e-9))
    >>> field = df.Field(mesh, dim=1, value=1e12)
    >>> exchange3 = mm.Exchange(A=field)

    """
    _allowed_attributes = ['A']
    _reprlatex = r'$A (\nabla \mathbf{m})^{2}$'

    def __repr__(self):
        return f'Exchange(A={self.A})'

    def energy(self, m):
        raise NotImplementedError

    def density(self, m):
        raise NotImplementedError

    def effective_field(self, m):
        raise NotImplementedError

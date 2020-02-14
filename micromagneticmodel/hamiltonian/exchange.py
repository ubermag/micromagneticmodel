import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(A=ts.Parameter(descriptor=ts.Scalar(unsigned=True),
                              otherwise=df.Field),
               name=ts.Name(const=True))
class Exchange(EnergyTerm):
    """Exchange energy term.

    It takes the exchange energy constant ``A`` and ``name`` as input
    parameters. Any further parameters, required by a specific
    micromagnetic calculator can be passed.

    Parameters
    ----------
    A : numbers.Real, dict, discretisedfield.Field

        If a single positive value ``numbers.Real`` is passed, spatially
        constant parameter is defined. For spatially varying parameter
        constant, either a dictionary, e.g. ``A={'region1': 1e-12,
        'region2': 5e-12}`` (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

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
    def __init__(self, A, name='exchange', **kwargs):
        self.A = A
        self.name = name
        self.__dict__.update(kwargs)

    def __repr__(self):
        """Representation string.

        Returns
        -------
        str

            Representation string.

        """
        return f'Exchange(A={self.A}, name=\'{self.name}\')'

    def _repr_latex_(self):
        """"LaTeX representation string, rendered inside Jupyter.

        """
        return r'$A (\nabla \mathbf{m})^{2}$'

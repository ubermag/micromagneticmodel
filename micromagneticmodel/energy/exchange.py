import discretisedfield as df
import ubermagutil as uu
import ubermagutil.typesystem as ts

from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(A=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field))
class Exchange(EnergyTerm):
    r"""Exchange energy term.

    .. math::

        w = - A \mathbf{m} \cdot \nabla^{2} \mathbf{m}

    Parameters
    ----------
    A : numbers.Real, dict, discretisedfield.Field

        If a single unsigned value ``numbers.Real`` is passed, a spatially
        constant parameter is defined. For a spatially varying parameter,
        either a dictionary, e.g. ``A={'region1': 1e-12, 'region2': 5e-12}``
        (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

    Examples
    --------
    1. Defining the exchange energy term using scalar.

    >>> import micromagneticmodel as mm
    ...
    >>> exchange = mm.Exchange(A=1e-12)

    2. Defining the exchange energy term using dictionary.

    >>> exchange = mm.Exchange(A={'region1': 1e-12, 'region2': 2e-12})

    3. Defining the exchange energy term using ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> A = df.Field(mesh, dim=1, value=5e-11)
    >>> exchange = mm.Exchange(A=A)

    4. An attempt to define the exchange energy term using a wrong value.

    >>> exchange = mm.Exchange(A='123')  # string value
    Traceback (most recent call last):
    ...
    TypeError: ...

    """
    _allowed_attributes = ["A"]
    _reprlatex = r"- A \mathbf{m} \cdot \nabla^{2} \mathbf{m}"

    def effective_field(self, m):
        raise NotImplementedError

import ubermagutil as uu
import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(H=ts.Parameter(descriptor=ts.Vector(size=3),
                              otherwise=df.Field))
class Zeeman(EnergyTerm):
    """Zeeman energy term.

    .. math::

        w_\\text{z} = -\\mu_{0}M_\\text{s} \\mathbf{m} \\cdot \\mathbf{H}

    Parameters
    ----------
    H : (3,) array_like, dict, discretisedfield.Field

        If a single length-3 array_like (tuple, list, ``numpy.ndarray``) is
        passed, which consists of ``numbers.Real``, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``H={'region1': (0, 0, 3e6), 'region2': (0, 0,
        -3e6)}`` (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

    Examples
    --------
    1. Defining the Zeeman energy term using a vector.

    >>> import micromagneticmodel as mm
    ...
    >>> zeeman = mm.Zeeman(H=(0, 0, 1e6))

    2. Defining the Zeeman energy term using dictionary.

    >>> zeeman = mm.Zeeman(H={'region1': (0, 0, 1e6), 'region2': (0, 0, -1e6)})

    3. Defining the Zeeman energy term using ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 10e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 10))
    >>> H = df.Field(mesh, dim=3, value=(1e6, -1e6, 0))
    >>> zeeman = mm.Zeeman(H=H)

    4. An attempt to define the Zeeman energy term using a wrong value.

    >>> zeeman = mm.Zeeman(H=(0, -1e7))  # length-2 vector
    Traceback (most recent call last):
    ...
    ValueError: ...

    """
    _allowed_attributes = ['H']
    _reprlatex = r'-\mu_{0}M_\text{s} \mathbf{m} \cdot \mathbf{H}'

    def effective_field(self, m):
        raise NotImplementedError

import ubermagutil as uu
import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(B1=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field),
               B2=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field),
               e=ts.Parameter(descriptor=ts.Vector(size=6),
                              otherwise=df.Field))
class MagnetoElastic(EnergyTerm):
    """Magneto-elastic energy term.

    .. math::

        w_\\text{mel} = B_{1}\\sum_{i} m_{i}\\epsilon_{ii} +
        B_{2}\\sum_{i}\\sum_{j\\ne i} m_{i}m_{j}\\epsilon_{ij}

    Parameters
    ----------
    B1/B2 : numbers.Real, dict, discretisedfield.Field

        If a single value ``numbers.Real`` is passed, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``B1={'region1': 1e7, 'region2': 5e7}`` (if the
        parameter is defined "per region") or ``discretisedfield.Field`` is
        passed.

    e : (6,) array_like, dict, discretisedfield.Field

        Symmetric strain matrix is assembled from the values of the vector e,
        so that eps11 = e[0], eps22=e[1], eps33=e[2], eps23=eps32=e[3],
        eps13=eps31=e[4], eps12=eps21=eps[5].

        If a single length-6 array_like (tuple, list, ``numpy.ndarray``) is
        passed, which consists of ``numbers.Real``, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``e={'region1': (1, 1, 1, 2, 3, 1), 'region2': (1, 1,
        2, 3, 2, 1)}`` (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

    Examples
    --------
    1. Defining the magneto-elastic energy term using single values.

    >>> import micromagneticmodel as mm
    ...
    >>> mel = mm.MagnetoElastic(B1=1e7, B2=1e7, e=(1, 1, 1, 1, 1, 1))

    2. Defining the magneto-elastic energy term using dictionary.

    >>> B1 = B2 = {'region1': 1e7, 'region2': 2e7}
    >>> e = {'region1': (1, 1, 1, 0, 0, 0), 'region2': (1, 1, 1, 1, 1, 1)}
    >>> mel = mm.MagnetoElastic(B1=B1, B2=B2, e=e)

    3. Defining the magneto-elastic energy term using
    ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> B1 = B2 = df.Field(mesh, dim=1, value=1e6)
    >>> e = df.Field(mesh, dim=6, value=(1, 1, 1, 1, 1, 1))
    >>> mel = mm.MagnetoElastic(B1=B1, B2=B2, e=e)

    4. An attempt to define the magneto-elastic energy term using a wrong
    value.

    >>> # length-3 e value
    >>> mel = mm.MagnetoElastic(B1=1e7, B2=2e7, e=(1, 1, 1))
    Traceback (most recent call last):
    ...
    ValueError: ...

    """
    _allowed_attributes = ['B1', 'B2', 'e']
    _reprlatex = (r'B_{1}\sum_{i} m_{i}\epsilon_{ii} + '
                  r'B_{2}\sum_{i}\sum_{j\ne i} m_{i}m_{j}\epsilon_{ij}')

    def effective_field(self, m):
        raise NotImplementedError

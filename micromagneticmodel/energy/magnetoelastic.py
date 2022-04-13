import discretisedfield as df
import ubermagutil as uu
import ubermagutil.typesystem as ts

from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(
    B1=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field),
    B2=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field),
    e_diag=ts.Parameter(descriptor=ts.Vector(size=3), otherwise=df.Field),
    e_offdiag=ts.Parameter(descriptor=ts.Vector(size=3), otherwise=df.Field),
)
class MagnetoElastic(EnergyTerm):
    r"""Magneto-elastic energy term.

    .. math::

        w = B_{1}\sum_{i} m_{i}\epsilon_{ii} + B_{2}\sum_{i}\sum_{j\ne i}
        m_{i}m_{j}\epsilon_{ij}

    Parameters
    ----------
    B1, B2 : numbers.Real, dict, discretisedfield.Field

        If a single value ``numbers.Real`` is passed, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``B1={'region1': 1e7, 'region2': 5e7}`` (if the
        parameter is defined "per region") or ``discretisedfield.Field`` is
        passed.

    e_diag/e_offdiag : (3,) array_like, dict, discretisedfield.Field

        Symmetric strain matrix is assembled from the values of the vector e,
        so that eps11 = e_diag[0], eps22=e_diag[1], eps33=e_diag[2],
        eps23=eps32=e_offdiag[0], eps13=eps31=e_offdiag[1],
        eps12=eps21=e_offdiag[2].

        If a single length-3 array_like (tuple, list, ``numpy.ndarray``) is
        passed, which consists of ``numbers.Real``, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``e={'region1': (1, 1, 1), 'region2': (1, 1, 1)}`` (if
        the parameter is defined "per region") or ``discretisedfield.Field`` is
        passed.

    Examples
    --------
    1. Defining the magneto-elastic energy term using single values.

    >>> import micromagneticmodel as mm
    ...
    >>> mel = mm.MagnetoElastic(B1=1e7, B2=1e7, e_diag=(1, 1, 1),
    ...                         e_offdiag=(0, 0, 0))

    2. Defining the magneto-elastic energy term using dictionary.

    >>> B1 = B2 = {'region1': 1e7, 'region2': 2e7}
    >>> e_diag = {'region1': (1, 1, 1), 'region2': (2, 2, 2)}
    >>> e_offdiag = {'region1': (0, 0, 0), 'region2': (0, 0, 0)}
    >>> mel = mm.MagnetoElastic(B1=B1, B2=B2, e_diag=e_diag,
    ...                         e_offdiag=e_offdiag)

    3. Defining the magneto-elastic energy term using
    ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> B1 = B2 = df.Field(mesh, dim=1, value=1e6)
    >>> e_diag = df.Field(mesh, dim=3, value=(1, 1, 1))
    >>> mel = mm.MagnetoElastic(B1=B1, B2=B2, e_diag=e_diag,
    ...                         e_offdiag=(0, 0, 0))

    4. An attempt to define the magneto-elastic energy term using a wrong
    value.

    >>> # length-3 e value
    >>> mel = mm.MagnetoElastic(B1=1e7, B2=2e7, e_diag=(1, 1, 1, 1))
    Traceback (most recent call last):
    ...
    ValueError: ...

    """
    _allowed_attributes = ["B1", "B2", "e_diag", "e_offdiag"]
    _reprlatex = (
        r"B_{1}\sum_{i} m_{i}\epsilon_{ii} + "
        r"B_{2}\sum_{i}\sum_{j\ne i} m_{i}m_{j}\epsilon_{ij}"
    )

    def effective_field(self, m):
        raise NotImplementedError

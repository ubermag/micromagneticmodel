import ubermagutil as uu
import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(K=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field),
               u=ts.Parameter(descriptor=ts.Vector(size=3),
                              otherwise=df.Field))
class UniaxialAnisotropy(EnergyTerm):
    """Uniaxial anisotropy energy term.

    .. math::

        w_\\text{ua} = -K (\\mathbf{m} \\cdot \\mathbf{u})^{2}

    Parameters
    ----------
    K : numbers.Real, dict, discretisedfield.Field

        If a single value ``numbers.Real`` is passed, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``K={'region1': 1e6, 'region2': 5e5}`` (if the
        parameter is defined "per region") or ``discretisedfield.Field`` is
        passed.

    u : (3,) array_like, dict, discretisedfield.Field

        If a single length-3 array_like (tuple, list, ``numpy.ndarray``) is
        passed, which consists of ``numbers.Real``, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``u={'region1': (0, 0, 1), 'region2': (1, 0, 0)}`` (if
        the parameter is defined "per region") or ``discretisedfield.Field`` is
        passed.

    Examples
    --------
    1. Defining the uniaxial anisotropy energy term using single values.

    >>> import micromagneticmodel as mm
    ...
    >>> ua = mm.UniaxialAnisotropy(K=1e5, u=(0, 0, 1))

    2. Defining the uniaxial anisotropy energy term using dictionary.

    >>> K = {'region1': 1e6, 'region2': 1e5}
    >>> u = {'region1': (0, 0, 1), 'region2': (1, 0, 0)}
    >>> ua = mm.UniaxialAnisotropy(K=K, u=u)

    3. Defining the uniaxial anisotropy energy term using
    ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> K = df.Field(mesh, dim=1, value=1e6)
    >>> u = df.Field(mesh, dim=3, value=(0, 1, 0))
    >>> ua = mm.UniaxialAnisotropy(K=K, u=u)

    4. An attempt to define the uniaxial anisotropy energy term using a wrong
    value.

    >>> ua = mm.UniaxialAnisotropy(K=1e5, u=(0, 0, 1, 0))  # length-4 vector
    Traceback (most recent call last):
    ...
    ValueError: ...

    """
    _allowed_attributes = ['K', 'u']
    _reprlatex = r'-K (\mathbf{m} \cdot \mathbf{u})^{2}'

    def effective_field(self, m):
        raise NotImplementedError

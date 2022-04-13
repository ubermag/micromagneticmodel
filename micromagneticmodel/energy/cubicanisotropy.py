import discretisedfield as df
import ubermagutil as uu
import ubermagutil.typesystem as ts

from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(
    K=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field),
    u1=ts.Parameter(descriptor=ts.Vector(size=3), otherwise=df.Field),
    u2=ts.Parameter(descriptor=ts.Vector(size=3), otherwise=df.Field),
)
class CubicAnisotropy(EnergyTerm):
    r"""Cubic anisotropy energy term.

    .. math::

        w = -K [(\mathbf{m} \cdot \mathbf{u}_{1})^{2}
                (\mathbf{m} \cdot \mathbf{u}_{2})^{2}
              + (\mathbf{m} \cdot \mathbf{u}_{2})^{2}
                (\mathbf{m} \cdot \mathbf{u}_{3})^{2}
              + (\mathbf{m} \cdot \mathbf{u}_{3})^{2}
                (\mathbf{m} \cdot \mathbf{u}_{1})^{2}]

    Parameters
    ----------
    K : numbers.Real, dict, discretisedfield.Field

        If a single value ``numbers.Real`` is passed, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``K={'region1': 1e6, 'region2': 5e5}`` (if the
        parameter is defined "per region") or ``discretisedfield.Field`` is
        passed.

    u1, u2 : (3,) array_like, dict, discretisedfield.Field

        If a single length-3 array_like (tuple, list, ``numpy.ndarray``) is
        passed, which consists of ``numbers.Real``, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``u1={'region1': (0, 0, 1), 'region2': (1, 0, 0)}``
        (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

    Examples
    --------
    1. Defining the cubic anisotropy energy term using single values.

    >>> import micromagneticmodel as mm
    ...
    >>> ca = mm.CubicAnisotropy(K=1e4, u1=(0, 0, 1), u2=(0, 1, 0))

    2. Defining the cubic anisotropy energy term using dictionary.

    >>> K = {'region1': 1e5, 'region2': 4e5}
    >>> u1 = {'region1': (0, 1, 1), 'region2': (0, 0, 1)}
    >>> u2 = {'region1': (0, -1, 1), 'region2': (0, 1, 0)}
    >>> ca = mm.CubicAnisotropy(K=K, u1=u1, u2=u2)

    3. Defining the cubic anisotropy energy term using
    ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> K = df.Field(mesh, dim=1, value=1e5)
    >>> u1 = df.Field(mesh, dim=3, value=(0, 1, 0))
    >>> u2 = df.Field(mesh, dim=3, value=(0, 0, 1))
    >>> ca = mm.CubicAnisotropy(K=K, u1=u1, u2=u2)

    4. An attempt to define the cubic anisotropy energy term using a wrong
    value.

    >>> # length-4 vector for u1
    >>> ca = mm.CubicAnisotropy(K=1e5, u1=(0, 0, 1, 0), u2=(1, 0, 0))
    Traceback (most recent call last):
    ...
    ValueError: ...

    """
    _allowed_attributes = ["K", "u1", "u2"]

    @property
    def _reprlatex(self):
        a1 = r"(\mathbf{m} \cdot \mathbf{u}_{1})^{2}"
        a2 = r"(\mathbf{m} \cdot \mathbf{u}_{2})^{2}"
        a3 = r"(\mathbf{m} \cdot \mathbf{u}_{3})^{2}"
        return r"-K [{0}{1}+{1}{2}+{2}{0}]".format(a1, a2, a3)

    def effective_field(self, m):
        raise NotImplementedError

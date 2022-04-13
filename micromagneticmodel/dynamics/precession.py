import discretisedfield as df
import ubermagutil as uu
import ubermagutil.typesystem as ts

from .dynamicsterm import DynamicsTerm


@uu.inherit_docs
@ts.typesystem(
    gamma0=ts.Parameter(descriptor=ts.Scalar(unsigned=True), otherwise=df.Field)
)
class Precession(DynamicsTerm):
    r"""Precession dynamics term.

    .. math::

        \frac{\text{d}\mathbf{m}}{\text{d}t} = -\frac{\gamma_{0}}{1 +
        \alpha^{2}} \mathbf{m} \times \mathbf{H}_\text{eff}

    Parameters
    ----------
    gamma0 : numbers.Real, dict, discretisedfield.Field

        If a single unsigned value ``numbers.Real`` is passed, a spatially
        constant parameter is defined. For a spatially varying parameter,
        either a dictionary, e.g. ``gamma={'region1': 1e5, 'region2': 5e5}``
        (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

    Examples
    --------
    1. Defining the precession dynamics term using scalar.

    >>> import micromagneticmodel as mm
    ...
    >>> precession = mm.Precession(gamma0=mm.consts.gamma0)

    2. Defining the precession dynamics term using dictionary.

    >>> precession = mm.Precession(gamma0={'region1': 1e5, 'region2': 2e6})

    3. Defining the precession dynamics term using ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> gamma0 = df.Field(mesh, dim=1, value=5e5)
    >>> precession = mm.Precession(gamma0=gamma0)

    4. An attempt to define the precession dynamics term using a wrong value.

    >>> precession = mm.Precession(gamma0=-5)  # negative value
    Traceback (most recent call last):
    ...
    ValueError: ...

    """
    _allowed_attributes = ["gamma0"]
    _reprlatex = (
        r"-\frac{\gamma_{0}}{1 + \alpha^{2}} \mathbf{m} "
        r"\times \mathbf{H}_\text{eff}"
    )

    def dmdt(self, m, Heff):
        raise NotImplementedError

import discretisedfield as df
import ubermagutil as uu
import ubermagutil.typesystem as ts

from .dynamicsterm import DynamicsTerm


@uu.inherit_docs
@ts.typesystem(
    alpha=ts.Parameter(descriptor=ts.Scalar(unsigned=True), otherwise=df.Field)
)
class Damping(DynamicsTerm):
    r"""Damping dynamics term.

    .. math::

        \frac{\text{d}\mathbf{m}}{\text{d}t} = -\frac{\gamma_{0}
        \alpha} {1 + \alpha^{2}} \mathbf{m} \times (\mathbf{m} \times
        \mathbf{H}_\text{eff})

    Parameters
    ----------
    alpha : numbers.Real, dict, discretisedfield.Field

        If a single positive value ``numbers.Real`` is passed, a spatially
        constant parameter is defined. For a spatially varying parameter,
        either a dictionary, e.g. ``alpha={'region1': 1e5, 'region2': 5e5}``
        (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

    Examples
    --------
    1. Defining the damping dynamics term using scalar.

    >>> import micromagneticmodel as mm
    ...
    >>> damping = mm.Damping(alpha=0.01)

    2. Defining the damping dynamics term using dictionary.

    >>> damping = mm.Damping(alpha={'region1': 0.01, 'region2': 0.005})

    3. Defining the damping dynamics term using ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> alpha = df.Field(mesh, dim=1, value=0.012)
    >>> damping = mm.Damping(alpha=alpha)

    4. An attempt to define the damping dynamics term using a wrong value.

    >>> damping = mm.Damping(alpha=-5)  # negative value
    Traceback (most recent call last):
    ...
    ValueError: ...

    """
    _allowed_attributes = ["alpha"]
    _reprlatex = (
        r"-\frac{\gamma_{0} \alpha}{1 + \alpha^{2}} \mathbf{m} "
        r"\times (\mathbf{m} \times \mathbf{H}_\text{eff})"
    )

    def dmdt(self, m, Heff):
        raise NotImplementedError

import ubermagutil as uu
import discretisedfield as df
import ubermagutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@uu.inherit_docs
@ts.typesystem(J=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field),
               mp=ts.Parameter(descriptor=ts.Vector(size=3),
                               otherwise=df.Field),
               Lambda=ts.Parameter(descriptor=ts.Scalar(positive=True),
                                   otherwise=df.Field),
               P=ts.Parameter(descriptor=ts.Scalar(positive=True),
                              otherwise=df.Field),
               eps_prime=ts.Parameter(descriptor=ts.Scalar(),
                                      otherwise=df.Field))
class Slonczewski(DynamicsTerm):
    """Slonczewski spin transfer torque dynamics term.

    .. math::

        \\frac{\\text{d}\\mathbf{m}}{\\text{d}t} =
        \\gamma_{0}\\beta\\epsilon(\\mathbf{m} \\times \\mathbf{m}_\\text{p}
        \\times \\mathbf{m}) - \\gamma_{0}\\beta\\epsilon' (\\mathbf{m} \\times
        \\mathbf{m}_\\text{p})

    .. math::

        \\beta = \\left| \\frac{\\hbar}{\\mu_{0}e} \\right|
        \\frac{J}{tM_\\text{s}}

    .. math::

        \\epsilon = \\frac{P\\Lambda^{2}}{(\\Lambda^{2} + 1) + (\\Lambda^{2} -
        1)(\\mathbf{m}\\cdot\\mathbf{m}_\\text{p})}

    Parameters
    ----------
    J : numbers.Real, dict, discretisedfield.Field

        If a single value ``numbers.Real`` is passed, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``J={'region1': 5e12, 'region2': 3e12}`` (if the
        parameter is defined "per region") or ``discretisedfield.Field`` is
        passed.

    mp : (3,) array_like, dict, discretisedfield.Field

        If a single vector value is passed, a spatially constant parameter is
        defined. For a spatially varying parameter, either a dictionary, e.g.
        ``mp={'region1': (0, 0, 1), 'region2': (0, 1, 0)}`` (if the parameter
        is defined "per region") or ``discretisedfield.Field`` is passed.

    P : numbers.Real, dict, discretisedfield.Field

        If a single positive value ``numbers.Real`` is passed, a spatially
        constant parameter is defined. For a spatially varying parameter,
        either a dictionary, e.g. ``P={'region1': 0.4, 'region2': 0.35}``
        (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

    Lambda : numbers.Real, dict, discretisedfield.Field

        If a single positive value ``numbers.Real`` is passed, a spatially
        constant parameter is defined. For a spatially varying parameter,
        either a dictionary, e.g. ``Lambda={'region1': 1.5, 'region2': 2}``
        (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

    eps_prime : numbers.Real, dict, discretisedfield.Field

        If a single value ``numbers.Real`` is passed, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``eps_prime={'region1': 0.4, 'region2': 0.35}`` (if
        the parameter is defined "per region") or ``discretisedfield.Field`` is
        passed. Defaults to 0.

    Examples
    --------
    1. Defining spatially constant Slonczewski dynamics term.

    >>> import micromagneticmodel as mm
    ...
    >>> slonczewski = mm.Slonczewski(J=7.5e12, mp=(1, 0, 0), P=0.4, Lambda=2)

    2. Defining spatially varying Slonczewski dynamics term.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> J = df.Field(mesh, dim=1, value=1e12)
    >>> slonczewski = mm.Slonczewski(J=J, mp=(1, 0, 0), P=0.4, Lambda=2,
    ...                              eps_prime=2)

    3. An attempt to define the Slonczewski dynamics term using a wrong value.

    >>> # scalar value for mp
    >>> slonczewski = mm.Slonczewski(J=J, mp=5, P=0.4, Lambda=2)
    Traceback (most recent call last):
    ...
    TypeError: ...

    """
    _allowed_attributes = ['J', 'mp', 'P', 'Lambda', 'eps_prime']

    @property
    def _reprlatex(self):
        reprlatex = (r'\gamma_{0}\beta\epsilon(\mathbf{m} \times '
                     r'\mathbf{m}_\text{p} \times \mathbf{m})')
        if hasattr(self, 'eps_prime'):
            if self.eps_prime:
                reprlatex += (r"-\gamma_{0}\beta\epsilon' (\mathbf{m} "
                              r"\times \mathbf{m}_\text{p})")

        return reprlatex

    def dmdt(self, m, Heff):
        raise NotImplementedError

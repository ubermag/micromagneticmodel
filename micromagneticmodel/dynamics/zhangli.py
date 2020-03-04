import ubermagutil as uu
import discretisedfield as df
import ubermagutil.typesystem as ts
from .dynamicsterm import DynamicsTerm


@uu.inherit_docs
@ts.typesystem(u=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field),
               beta=ts.Scalar())
class ZhangLi(DynamicsTerm):
    """Zhang-Li spin transfer torque dynamics term.

    .. math::

        \\frac{\\text{d}\\mathbf{m}}{\\text{d}t} = -(\\mathbf{u} \\cdot
        \\boldsymbol\\nabla)\\mathbf{m} + \\beta\\mathbf{m} \\times
        \\big[(\\mathbf{u} \\cdot \\boldsymbol\\nabla)\\mathbf{m}\\big]

    Parameters
    ----------
    beta : numbers.Real

        A single scalar value can be passed.

    u : number.Real, discretisedfield.Field

        `numbers.Real` can be passed, or alternatively
        ``discretisedfield.Field`` can be passed.

    Examples
    --------
    1. Defining the Zhang-Li dynamics term using scalar.

    >>> import micromagneticmodel as mm
    ...
    >>> zhangli = mm.ZhangLi(beta=0.01, u=5e6)

    2. Defining the Zhang-Li dynamics term using ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> beta = 0.012
    >>> u = df.Field(mesh, dim=1, value=1e5)
    >>> zhangli = mm.ZhangLi(beta=beta, u=u)

    3. An attempt to define the Zhang-Li dynamics term using a wrong value.

    >>> zhangli = mm.ZhangLi(beta=-1, u=(0, 0, 1))  # vector value
    Traceback (most recent call last):
    ...
    TypeError: ...

    """
    _allowed_attributes = ['u', 'beta']
    _reprlatex = (r'-(\mathbf{u} \cdot \boldsymbol\nabla)\mathbf{m} + '
                  r'\beta\mathbf{m} \times \big[(\mathbf{u} \cdot '
                  r'\boldsymbol\nabla)\mathbf{m}\big]')

    def dmdt(self, m, Heff):
        raise NotImplementedError

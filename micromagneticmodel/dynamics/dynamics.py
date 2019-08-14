import micromagneticmodel as mm
from .dynamicsterm import DynamicsTerm


class Dynamics(mm.util.TermSum):
    """Dynamics equation class.

    This class implements the sum of individual dynamics terms.

    Examples
    --------
    1. Setting up the dynamics equation.

    >>> import micromagneticmodel as mm
    ...
    >>> dynamics = mm.Dynamics()
    >>> dynamics += mm.Precession(gamma=mm.consts.gamma0)
    >>> dynamics += mm.Damping(alpha=0.1)

    """
    _lefthandside = r'$\frac{\partial \mathbf{m}}{\partial t}='
    _terms_type = DynamicsTerm

import ubermagutil as uu

import micromagneticmodel as mm

from .dynamicsterm import DynamicsTerm


@uu.inherit_docs
class Dynamics(mm.abstract.Container):
    """Dynamics terms container class.

    Parameters
    ----------
    terms : list

        A list of dynamics terms.

    Examples
    --------
    1. Defining dynamics terms container.

    >>> import micromagneticmodel as mm
    ...
    >>> terms = [mm.Precession(gamma0=mm.consts.gamma0), mm.Damping(alpha=0.1)]
    >>> dynamics = mm.Dynamics(terms=terms)
    >>> len(dynamics)  # the number of terms
    2

    """

    _term_class = DynamicsTerm

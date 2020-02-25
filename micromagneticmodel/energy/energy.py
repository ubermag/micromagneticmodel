import ubermagutil as uu
import micromagneticmodel as mm
from .energyterm import EnergyTerm


@uu.inherit_docs
class Energy(mm.util.TermsContainer):
    """Energy terms container class.

    Parameters
    ----------
    terms : list

        A list of energy terms.

    Examples
    --------
    1. Defining energy terms container.

    >>> import micromagneticmodel as mm
    ...
    >>> terms = [mm.Exchange(A=1e-12), mm.Demag()]
    >>> energy = mm.Energy(terms=terms)
    >>> len(energy)  # the number of terms
    2

    """
    _lhslatex = 'w ='
    _terms_class = EnergyTerm

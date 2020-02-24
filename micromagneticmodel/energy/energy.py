import micromagneticmodel as mm
from .energyterm import EnergyTerm


class Energy(mm.util.TermSum):
    """Hamiltonian class.

    This class implements the sum of individual energy terms.

    Examples
    --------
    1. Setting up the Hamiltonian.

    >>> import micromagneticmodel as mm
    ...
    >>> hamiltonian = mm.Hamiltonian()
    >>> hamiltonian += mm.DMI(D=1e-3, crystalclass='Cnv')
    >>> hamiltonian += mm.Exchange(A=1e-12)

    """
    _lefthandside = '$w='
    _terms_type = EnergyTerm

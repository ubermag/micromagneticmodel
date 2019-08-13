import micromagneticmodel as mm
from .energyproperties import EnergyProperties


class EnergyTerm(mm.util.Term, EnergyProperties):
    """EnergyTerm class from which all energy terms are derived.

    This class is a derived class from `micromagneticmodel.util.Term`
    and `micromagneticmodel.EnergyProperties`.

    """
    _termsum_type = 'Hamiltonian'

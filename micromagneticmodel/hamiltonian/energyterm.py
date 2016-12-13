import micromagneticmodel as mm
from .energyproperties import EnergyProperties


class EnergyTerm(mm.util.Term, EnergyProperties):
    _termsum_type = "Hamiltonian"

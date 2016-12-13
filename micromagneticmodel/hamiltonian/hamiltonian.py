import micromagneticmodel as mm
from .energyproperties import EnergyProperties
from .energyterm import EnergyTerm


class Hamiltonian(mm.util.TermSum, EnergyProperties):
    _lefthandside = '$\\mathcal{H}='
    _terms_type = EnergyTerm

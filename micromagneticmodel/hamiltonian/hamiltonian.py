import micromagneticmodel as mm
from .energyterm import EnergyTerm
from .energyproperties import EnergyProperties


class Hamiltonian(mm.util.TermSum, EnergyProperties):
    _lefthandside = '$\\mathcal{H}='
    _terms_type = EnergyTerm

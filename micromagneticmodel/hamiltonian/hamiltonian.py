import micromagneticmodel as mm
from .energyterm import EnergyTerm


class Hamiltonian(mm.util.TermSum):
    _lefthandside = '$\\mathcal{H}='
    _terms_type = EnergyTerm

    @property
    def energy(self):
        raise NotImplementedError

    @property
    def energy_density(self):
        raise NotImplementedError

    @property
    def effective_field(self):
        raise NotImplementedError

import micromagneticmodel as mm


class EnergyTerm(mm.util.Term):
    """Class from which all energy terms are derived.

    """
    _termsum_type = mm.Hamiltonian

    def energy(self):
        pass

    def energy_density(self):
        pass

    def effective_field(self):
        pass

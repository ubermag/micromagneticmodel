import micromagneticmodel as mm


class EnergyTerm(mm.util.Term):
    """A class for deriving all energy terms.

    """
    _termsum_type = mm.Energy

    def energy(self):
        pass

    def density(self):
        pass

    def effective_field(self):
        pass

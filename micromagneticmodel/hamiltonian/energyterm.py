import micromagneticmodel as mm


class EnergyTerm(mm.util.Term):
    def __add__(self, other):
        """Addition for creating a sum of energy terms."""
        from .hamiltonian import Hamiltonian
        hamiltonian = Hamiltonian()
        hamiltonian.add(self)
        hamiltonian.add(other)
        return hamiltonian

import hamiltonian
from micromagneticmodel.util import Term


class EnergyTerm(Term):
    def __add__(self, other):
        """Addition for creating a list of energy objects."""
        result = hamiltonian.Hamiltonian()
        result.add(self)
        result.add(other)
        return result

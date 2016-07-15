from micromagneticmodel.util import Term
from hamiltonian import Hamiltonian


class EnergyTerm(Term):
    def __add__(self, other):
        """Addition for creating a list of energy objects."""
        hamiltonian = Hamiltonian()
        hamiltonian.add(self)
        hamiltonian.add(other)
        return hamiltonian

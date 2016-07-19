from micromagneticmodel.util import Term


class EnergyTerm(Term):
    def __add__(self, other):
        """Addition for creating a list of energy objects."""
        from micromagneticmodel.hamiltonian import Hamiltonian
        hamiltonian = Hamiltonian()
        hamiltonian.add(self)
        hamiltonian.add(other)
        return hamiltonian

from micromagneticmodel.util import TermSum
from micromagneticmodel.hamiltonian.energyterm import EnergyTerm


class Hamiltonian(TermSum):
    _lefthandside = '$\\mathcal{H}='

    def add(self, term):
        """Add an energy term to hamiltonian.

        Args:
            term (EnergyTerm): energy term to be added

        """
        if not isinstance(term, EnergyTerm):
            raise TypeError("Only EnergyTerm and Hamiltonian objects"
                            "can be added to hamiltonian.")
        self.terms.append(term)

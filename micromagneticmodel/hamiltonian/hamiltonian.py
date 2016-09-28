from micromagneticmodel.util import TermSum
from micromagneticmodel.hamiltonian.energyterm import EnergyTerm


class Hamiltonian(TermSum):
    _lefthandside = '$\\mathcal{H}='

    def add(self, value):
        """Add an energy term to hamiltonian.

        Args:
            value (EnergyTerm, Hamiltonian): energy term or hamiltonian
              to be added

        """
        if isinstance(value, EnergyTerm):
            self.terms.append(value)
        elif isinstance(value, self.__class__):
            for term in value.terms:
                self.terms.append(term)
        else:
            raise TypeError("Only EnergyTerm or Hamiltonian objects"
                            "can be added to hamiltonian.")

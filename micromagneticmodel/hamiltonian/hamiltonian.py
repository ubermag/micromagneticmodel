from micromagneticmodel.hamiltonian import energyterm
from micromagneticmodel.util import TermSum


class Hamiltonian(TermSum):
    _lefthandside = '$\\mathcal{H}='

    def add(self, term):
        """Add an energy term to hamiltonian.

        Args:
            term (EnergyTerm): energy term to be added

        """
        if not isinstance(term, energyterm.EnergyTerm):
            raise TypeError('Only energy terms can be added to hamiltonian.')
        self.terms.append(term)

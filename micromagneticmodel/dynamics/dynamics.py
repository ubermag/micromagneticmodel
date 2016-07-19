from micromagneticmodel.dynamics import DynamicsTerm
from micromagneticmodel.util import TermSum


class Dynamics(TermSum):
    _lefthandside = '$\\frac{\partial \mathbf{m}}{\partial t}='
    
    def add(self, term):
        """Add a dynamics term to hamiltonian.

        Args:
            term (DynamicsTerm): dynamics term to be added

        """
        if not isinstance(term, DynamicsTerm):
            raise TypeError("Only dynamics terms can be added to the "
                            "equation of motion.")
        self.terms.append(term)

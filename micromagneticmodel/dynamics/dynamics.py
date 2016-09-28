import micromagneticmodel as mm
from .dynamicsterm import DynamicsTerm


class Dynamics(mm.util.TermSum):
    _lefthandside = '$\\frac{\partial \mathbf{m}}{\partial t}='

    def add(self, value):
        """Add a dynamics term to dynamics.

        Args:
            value (DynamicsTerm, Dynamics): dynamics term or dynamics
              to be added

        """
        if isinstance(value, DynamicsTerm):
            self.terms.append(value)
        elif isinstance(value, self.__class__):
            for term in value.terms:
                self.terms.append(term)
        else:
            raise TypeError("Only DynamicsTerm or Dynamics objects"
                            "can be added to dynamics.")

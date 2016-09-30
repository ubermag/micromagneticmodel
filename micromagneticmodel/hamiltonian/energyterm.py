import importlib
import micromagneticmodel as mm


class EnergyTerm(mm.util.Term):
    def __add__(self, other):
        """Addition for creating a sum of energy terms."""
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        hamiltonian = self.selfmodule.Hamiltonian()
        hamiltonian.add(self)
        hamiltonian.add(other)
        return hamiltonian

    def energy(self):
        raise NotImplementedError

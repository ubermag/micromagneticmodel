import importlib
import micromagneticmodel as mm


class DynamicsTerm(mm.util.Term):
    def __add__(self, other):
        """Addition for creating a sum of dynamics terms."""
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        dynamics = self.selfmodule.Dynamics()
        dynamics.add(self)
        dynamics.add(other)
        return dynamics

import micromagneticmodel as mm


class DynamicsTerm(mm.util.Term):
    def __add__(self, other):
        """Addition for creating a sum of dynamics terms."""
        from .dynamics import Dynamics
        dynamics = Dynamics()
        dynamics.add(self)
        dynamics.add(other)
        return dynamics

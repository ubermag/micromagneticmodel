from micromagneticmodel.util import Term


class DynamicsTerm(Term):
    def __add__(self, other):
        """Addition for creating a sum of dynamics terms."""
        from micromagneticmodel.dynamics import Dynamics
        dynamics = Dynamics()
        dynamics.add(self)
        dynamics.add(other)
        return dynamics

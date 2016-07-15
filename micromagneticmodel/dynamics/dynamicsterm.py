from micromagneticmodel.util import Term
from dynamics import Dynamics


class DynamicsTerm(Term):
    def __add__(self, other):
        """Addition for creating a list of energy objects."""
        dynamics = Dynamics()
        dynamics.add(self)
        dynamics.add(other)
        return dynamics

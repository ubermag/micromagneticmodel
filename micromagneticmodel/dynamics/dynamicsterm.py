import dynamics
from micromagneticmodel.util import Term


class DynamicsTerm(Term):
    def __add__(self, other):
        """Addition for creating a list of energy objects."""
        result = dynamics.Dynamics()
        result.add(self)
        result.add(other)
        return result

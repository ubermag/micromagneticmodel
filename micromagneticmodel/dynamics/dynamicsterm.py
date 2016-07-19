from micromagneticmodel.util import Term


class DynamicsTerm(Term):
    def __add__(self, other):
        """Addition for creating a list of energy objects."""
        from micromagneticmodel.dynamics import Dynamics
        result = Dynamics()
        result.add(self)
        result.add(other)
        return result

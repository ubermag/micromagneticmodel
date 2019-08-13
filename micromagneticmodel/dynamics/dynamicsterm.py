import micromagneticmodel as mm


class DynamicsTerm(mm.util.Term):
    """DynamicsTerm class from which all dynamics terms are derived.

    This class is a derived class from `micromagneticmodel.util.Term`.

    """
    _termsum_type = 'Dynamics'

import micromagneticmodel as mm


class Dynamics(mm.util.TermSum):
    _lefthandside = '$\\frac{\partial \mathbf{m}}{\partial t}='
    _terms_type = "DynamicsTerm"

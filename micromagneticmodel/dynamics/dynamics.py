import micromagneticmodel as mm
from .dynamicsterm import DynamicsTerm


class Dynamics(mm.util.TermSum):
    _lefthandside = '$\\frac{\partial \mathbf{m}}{\partial t}='
    _terms_type = DynamicsTerm

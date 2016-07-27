from micromagneticmodel.hamiltonian import EnergyTerm


class Demag(EnergyTerm):
    _name = 'demag'
    _latex_str = ("$-\\frac{1}{2}\mu_{0}M_\\text{s}"
                  "\mathbf{m} \cdot \mathbf{H}_\\text{d}$")

    def __init__(self):
        """Abstract demagnetisation energy class."""
        pass

    def __repr__(self):
        """A representation method."""
        return "Demag()"
    
    def script(self):
        """This method should be provided by the specific micromagnetic
        calculator"""
        raise NotImplementedError

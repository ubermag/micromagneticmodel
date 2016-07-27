from micromagneticmodel.hamiltonian import EnergyTerm


class Demag(EnergyTerm):
    _name = "demag"
    _latex_str = ("$-\\frac{1}{2}\mu_{0}M_\\text{s}"
                  "\mathbf{m} \cdot \mathbf{H}_\\text{d}$")

    def __init__(self):
        """Abstract demagnetisation energy class."""
        pass
    
    def script(self):
        """This method should be provided by the specific micromagnetic
        calculator"""
        raise NotImplementedError

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "Demag()"

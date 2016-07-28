from micromagneticmodel.hamiltonian import EnergyTerm


class Demag(EnergyTerm):
    _name = "demag"
    _latex_str = ("$-\\frac{1}{2}\mu_{0}M_\\text{s}"
                  "\mathbf{m} \cdot \mathbf{H}_\\text{d}$")

    def __init__(self):
        """Abstract demagnetisation energy class."""
        pass

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return "Demag()"

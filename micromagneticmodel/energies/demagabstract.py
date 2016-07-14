from energyterm import EnergyTerm


class DemagAbstract(EnergyTerm):
    latex_str = ("$-\\frac{1}{2}\mu_{0}M_\\text{s}"
                 "\mathbf{m} \cdot \mathbf{H}_\\text{d}$")

    def __init__(self):
        """Abstract demagnetisation energy class."""
        pass

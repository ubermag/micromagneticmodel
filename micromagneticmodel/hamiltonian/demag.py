import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@ts.typesystem(name=ts.Name(const=True))
class Demag(EnergyTerm):
    _latex = (r'$-\frac{1}{2}\mu_{0}M_\text{s}'
              r'\mathbf{m} \cdot \mathbf{H}_\text{d}$')

    def __init__(self, name='demag', **kwargs):
        """Micromagnetic demagnetisation energy term.

        This object models micromagnetic exchange energy term. It does
        not take any mandatory arguments. However, any parameters
        required by a specific micromagnetic calculator can be passed.

        Examples
        --------
        1. Initialising the demagnetisation energy term.

        >>> import micromagneticmodel as mm
        ...
        >>> demag = mm.Demag()

        """
        self.name = name
        self.__dict__.update(kwargs)

    @property
    def _repr(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return f'Demag(name=\'{self.name}\')'

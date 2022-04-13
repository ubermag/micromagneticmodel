import ubermagutil as uu
import ubermagutil.typesystem as ts

from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(
    sigma=ts.Scalar(),
    sigma2=ts.Scalar(),
    subregions=ts.Typed(expected_type=(list, tuple, set)),
)
class RKKY(EnergyTerm):
    """RKKY energy term.

    This class defines RKKY interaction between two closest (mutually facing)
    surfaces of subregions defined by passing ``subregions`` list.

    Parameters
    ----------
    sigma : numbers.Real, optional

        Bilinear surface (interfacial) exchange energy constant.

    sigma2 : numbers.Real, optional

        Biquadratic surface (interfacial) exchange energy constant.

    subregions : list, tuple, set

        Length-2 list of strings, which are the names of two interacting
        regions.

    Examples
    --------
    1. Defining the RKKY energy term between two subregions.

    >>> import micromagneticmodel as mm
    ...
    >>> rkky = mm.RKKY(sigma=-1e-4, subregions=['r1', 'r2'])

    4. An attempt to define the RKKY energy term using a wrong value.

    >>> rkky = mm.RKKY(sigma=-1e-4, subregions='r1')
    Traceback (most recent call last):
    ...
    TypeError: ...

    """

    _allowed_attributes = ["sigma", "sigma2", "subregions"]

    @property
    def _reprlatex(self):
        return r"\text{{RKKY}}" r"(\text{{{}}}, \text{{{}}})".format(*self.subregions)

    def effective_field(self, m):
        raise NotImplementedError

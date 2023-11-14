import discretisedfield as df
import ubermagutil as uu
import ubermagutil.typesystem as ts

from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(Gamma=ts.Parameter(descriptor=ts.Scalar(), otherwise=df.Field))
class AEI(EnergyTerm):
    r"""AEI energy term."""
    _allowed_attributes = ["Gamma", "nn"]
    _reprlatex = r"-"

    def effective_field(self, m):
        raise NotImplementedError

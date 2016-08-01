from micromagneticmodel.hamiltonian import EnergyTerm
from micromagneticmodel.util.typesystem import RealVector3D, UnsignedReal, \
    String, typesystem


@typesystem(H=RealVector3D,
            name=String,
            latex_str=String)
class Zeeman(EnergyTerm):
    def __init__(self, H, name='zeeman'):
        """A Zeeman energy class.

        This method internally calls set_H method. Refer to its documentation.

        """
        self.H = H
        self.name = name
        self.latex_str = '$-\mu_{0}M_\\text{s} \mathbf{m} \cdot \mathbf{H}$'

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return 'Zeeman(H={})'.format(self.H)

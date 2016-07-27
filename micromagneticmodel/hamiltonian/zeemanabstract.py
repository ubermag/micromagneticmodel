import abc
import numpy as np
from numbers import Real
from micromagneticmodel.hamiltonian import EnergyTerm


class ZeemanAbstract(EnergyTerm):
    _name = "zeeman"
    _latex_str = "$-\mu_{0}M_\\text{s} \mathbf{m} \cdot \mathbf{H}$"

    def __init__(self, H):
        """A Zeeman energy class.

        This method internally calls set_H method. Refer to its documentation.

        """
        self.set_H(H)

    def set_H(self, H):
        """A method for setting the external magnetic field value

        Args:
            H (tuple, list, np.ndarray): external magnetic field (A/m)

        """
        if not isinstance(H, (list, tuple, np.ndarray)) or len(H) != 3:
            raise ValueError('H must be a 3-element tuple, '
                             'list, or np.ndarray.')
        if not all([isinstance(i, Real) for i in H]):
            raise ValueError('All elements of H must be real numbers.')
        self.H = H

    @property
    def _repr_str(self):
        """A representation string property.
        
        Returns:
           A representation string.

        """
        return "Zeeman(H={})".format(self.H)

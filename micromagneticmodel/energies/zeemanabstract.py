import abc
import numpy as np
from numbers import Real
from energyterm import EnergyTerm


class ZeemanAbstract(EnergyTerm):
    latex_str = '$-\mu_{0}M_\\text{s} \mathbf{m} \cdot \mathbf{H}$'
    
    def __init__(self, H):
        """A Zeeman energy class.

        Args:
            H (tuple, list, np.ndarray): external magnetic field (A/m)

        """
        self.set_H(H)
        
    def set_H(self, H):
        if not isinstance(H, (list, tuple, np.ndarray)) or len(H) != 3:
            raise ValueError('H must be a 3-element tuple or list.')
        if not all([isinstance(i, Real) for i in H]):
            raise ValueError('All elements of H must be real numbers.')
        self.H = H

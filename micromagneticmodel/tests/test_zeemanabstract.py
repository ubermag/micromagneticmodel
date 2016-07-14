import pytest
import numpy as np
from numbers import Real
from micromagneticmodel.energies import ZeemanAbstract


class Zeeman(ZeemanAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        raise NotImplementedError()


class TestZeemanAbstract(object):
    def setup(self):
        self.valid_args = [(1, 1.4, 1),
                           (0, 0, 1),
                           [1.2, 0, 0],
                           (0.56e6, 1.98e6, -1.1e7),
                           np.array([15e6, 0, 5e-8])]
        self.invalid_args = [(1, 1),
                             1,
                             (1.2, 0, 0, 5),
                             (0.56, 1.98, '-1.1'),
                             ([15], [0], [np.pi])]

    def test_init_valid_args(self):
        for H in self.valid_args:
            zeeman = Zeeman(H)

            assert isinstance(zeeman.H, (tuple, list, np.ndarray))
            assert len(zeeman.H) == 3
            assert all([isinstance(i, Real) for i in zeeman.H])

    def test_init_invalid_args(self):
        for H in self.invalid_args:
            with pytest.raises(ValueError):
                zeeman = Zeeman(H)

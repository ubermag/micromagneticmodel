import pytest
import numpy as np
from numbers import Real
from micromagneticmodel.hamiltonian import ZeemanAbstract


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

    def test_abstract_class(self):
        for H in self.valid_args:
            with pytest.raises(TypeError):
                zeemanabstract = ZeemanAbstract(H)

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

    def test_repr_latex(self):
        for H in self.valid_args:
            zeeman = Zeeman(H)
            latex_str = zeeman._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex_str, str)
            assert latex_str[0] == latex_str[-1] == '$'
            assert latex_str[1] == '-'
            assert '\\mu_{0}' in latex_str
            assert '\mathbf{H}' in latex_str
            assert '\mathbf{m}' in latex_str
            assert '\cdot' in latex_str
            assert 'M_\\text{s}' in latex_str

    def test_name(self):
        for H in self.valid_args:
            zeeman = Zeeman(H)

            assert zeeman._name == 'zeeman'

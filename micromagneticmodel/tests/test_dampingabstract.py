import pytest
from numbers import Real
from micromagneticmodel.dynamics import DampingAbstract


class Damping(DampingAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        raise NotImplementedError()


class TestDampingAbstract(object):
    def setup(self):
        self.valid_args = [1, 2.0, 5e-11, 1e-12, 1e-13, 1e-14, 1e6]
        self.invalid_args = [-1, -2.1, 'a', (1, 2), -3.6e-6, '0', [1, 2, 3]]

    def test_abstract_class(self):
        for alpha in self.valid_args:
            with pytest.raises(TypeError):
                dampingabstract = DampingAbstract(alpha)

    def test_init_valid_args(self):
        for alpha in self.valid_args:
            damping = Damping(alpha)

            assert damping.alpha == alpha
            assert isinstance(damping.alpha, Real)

    def test_init_invalid_args(self):
        for alpha in self.invalid_args:
            with pytest.raises(ValueError):
                damping = Damping(alpha)

    def test_repr_latex_(self):
        for alpha in self.valid_args:
            damping = Damping(alpha)
            latex_str = damping._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex_str, str)
            assert latex_str[0] == latex_str[-1] == '$'
            assert '\\alpha' in latex_str
            assert '\mathbf{m}' in latex_str
            assert '\\frac' in latex_str
            assert '\\times' in latex_str
            assert latex_str.count('\partial') == 2

    def test_name(self):
        for alpha in self.valid_args:
            damping = Damping(alpha)

            assert damping._name == 'damping'

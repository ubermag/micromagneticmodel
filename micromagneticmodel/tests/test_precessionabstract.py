import pytest
from numbers import Real
from micromagneticmodel.dynamics import PrecessionAbstract


class Precession(PrecessionAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        raise NotImplementedError()


class TestPrecessionAbstract(object):
    def setup(self):
        self.valid_args = [1, 2.0, 5e-11, 1e-12, 1e-13, 1e-14, 1e6]
        self.invalid_args = [-1, -2.1, 'a', (1, 2), -3.6e-6, '0', [1, 2, 3]]

    def test_abstract_class(self):
        for gamma in self.valid_args:
            with pytest.raises(TypeError):
                precessionabstract = PrecessionAbstract(gamma)

    def test_init_valid_args(self):
        for gamma in self.valid_args:
            precession = Precession(gamma)

            assert precession.gamma == gamma
            assert isinstance(precession.gamma, Real)

    def test_init_invalid_args(self):
        for gamma in self.invalid_args:
            with pytest.raises(ValueError):
                precession = Precession(gamma)

    def test_repr_latex_(self):
        for gamma in self.valid_args:
            precession = Precession(gamma)
            latex_str = precession._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex_str, str)
            assert latex_str[0] == latex_str[-1] == '$'
            assert '\gamma' in latex_str
            assert '\mathbf{m}' in latex_str
            assert '\mathbf{H}_\\text{eff}' in latex_str
            assert '\\times' in latex_str

    def test_name(self):
        for gamma in self.valid_args:
            precession = Precession(gamma)

            assert precession._name == 'precession'

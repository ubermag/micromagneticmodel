import pytest
import numbers
import micromagneticmodel as mm


class TestPrecession(object):
    def setup(self):
        self.valid_args = [1, 2.0, 5e-11, 1e-12, 1e-13, 1e-14, 1e6]
        self.invalid_args = [-1, -2.1, 'a', (1, 2), -3.6e-6, '0', [1, 2, 3]]

    def test_init_valid_args(self):
        for gamma in self.valid_args:
            precession = mm.Precession(gamma)
            assert precession.gamma == gamma
            assert isinstance(precession.gamma, numbers.Real)

    def test_init_invalid_args(self):
        for gamma in self.invalid_args:
            with pytest.raises(Exception):
                precession = mm.Precession(gamma)

    def test_repr_latex_(self):
        for gamma in self.valid_args:
            precession = mm.Precession(gamma)
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
            precession = mm.Precession(gamma)
            assert precession.name == 'precession'

    def test_repr(self):
        for gamma in self.valid_args:
            precession = mm.Precession(gamma)
            assert repr(precession) == 'Precession(gamma={})'.format(gamma)

        precession = mm.Precession(2.211e5)
        assert repr(precession) == 'Precession(gamma=221100.0)'

    def test_script(self):
        for gamma in self.valid_args:
            precession = mm.Precession(gamma)
            with pytest.raises(NotImplementedError):
                precession.script()

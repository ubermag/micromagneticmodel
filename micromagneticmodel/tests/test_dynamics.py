import pytest
from micromagneticmodel.dynamics import PrecessionAbstract, \
    DampingAbstract, Dynamics


class Precession(PrecessionAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        return 'precession_script\n'


class Damping(DampingAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        return 'damping_script\n'


class TestDynamics(object):
    def setup(self):
        gamma = 2.21e5
        self.precession = Precession(gamma)
        alpha = 0.5
        self.damping = Damping(alpha)

        self.terms = [self.precession,
                      self.damping]

        self.invalid_terms = [1, 2.5, 0, 'abc', [3, 7e-12],
                              [self.precession, self.damping]]

    def test_add(self):
        dynamics = Dynamics()
        for term in self.terms:
            dynamics.add(term)

            assert isinstance(dynamics, Dynamics)
            assert isinstance(dynamics.terms, list)
            assert dynamics.terms[-1] == term
            assert dynamics.terms[-1]._name == term._name

        assert len(dynamics.terms) == 2

    def test_add_sum(self):
        dynamics = self.precession + self.damping

        assert isinstance(dynamics, Dynamics)
        assert isinstance(dynamics.terms, list)
        assert len(dynamics.terms) == 2

    def test_iadd(self):
        dynamics = Dynamics()
        for term in self.terms:
            dynamics += term

            assert isinstance(dynamics, Dynamics)
            assert isinstance(dynamics.terms, list)
            assert dynamics.terms[-1] == term
            assert dynamics.terms[-1]._name == term._name

        assert len(dynamics.terms) == 2

    def test_repr_latex(self):
        dynamics = Dynamics()
        latex_str = dynamics._repr_latex_()
        assert latex_str[0] == latex_str[-1] == '$'
        assert latex_str.count('$') == 2
        assert '\\frac' in latex_str
        assert latex_str[-2] == '0'

        for term in self.terms:
            dynamics.add(term)

        latex_str = dynamics._repr_latex_()

        assert latex_str[0] == latex_str[-1] == '$'
        assert latex_str.count('$') == 2
        assert '-\gamma' in latex_str
        assert '\mathbf{m}' in latex_str
        assert '\mathbf{H}_\\text{eff}' in latex_str
        assert '\\times' in latex_str
        assert '\\alpha' in latex_str
        assert latex_str.count('-') == 1
        assert latex_str.count('+') == 1
        assert latex_str.count('=') == 1
        assert latex_str.count('\partial') == 4

    def test_add_exception(self):
        dynamics = Dynamics()
        for term in self.invalid_terms:
            with pytest.raises(TypeError):
                dynamics += term

    def test_calculator_script(self):
        dynamics = self.precession + self.damping

        calculator_script = dynamics.calculator_script()

        assert isinstance(calculator_script, str)
        assert 'precession_script' in calculator_script
        assert 'damping_script' in calculator_script
        assert calculator_script.count('\n') == 2

    def test_repr(self):
        gamma = 2.21e5
        self.precession = Precession(gamma)
        alpha = 0.5
        dynamics = self.precession + self.damping

        exp_str = ("Precession(gamma=221000.0) + "
                   "Damping(alpha=0.5)")
        assert repr(dynamics) == exp_str

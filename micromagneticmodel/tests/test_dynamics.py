import pytest
import micromagneticmodel as mm


class TestDynamics(object):
    def setup(self):
        gamma = 2.21e5
        self.precession = mm.Precession(gamma)
        alpha = 0.5
        self.damping = mm.Damping(alpha)

        self.terms = [self.precession,
                      self.damping]

        self.invalid_terms = [1, 2.5, 0, 'abc', [3, 7e-12],
                              [self.precession, self.damping]]

    def test_add_terms(self):
        dynamics = mm.Dynamics()
        for term in self.terms:
            dynamics.add(term)
            assert isinstance(dynamics, mm.Dynamics)
            assert isinstance(dynamics.terms, list)
            assert dynamics.terms[-1] == term
            assert dynamics.terms[-1].name == term.name

        assert len(dynamics.terms) == 2

    def test_add_sum_of_terms(self):
        dynamics = self.precession + self.damping

        assert isinstance(dynamics, mm.Dynamics)
        assert isinstance(dynamics.terms, list)
        assert len(dynamics.terms) == 2

    def test_add_dynamics(self):
        term_sum = self.precession + self.damping
        dynamics = mm.Dynamics()
        dynamics += term_sum

        assert len(dynamics.terms) == 2

    def test_iadd(self):
        dynamics = mm.Dynamics()
        for term in self.terms:
            dynamics += term

            assert isinstance(dynamics, mm.Dynamics)
            assert isinstance(dynamics.terms, list)
            assert dynamics.terms[-1] == term
            assert dynamics.terms[-1].name == term.name

        assert len(dynamics.terms) == 2

    def test_repr_latex(self):
        dynamics = mm.Dynamics()
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
        dynamics = mm.Dynamics()
        for term in self.invalid_terms:
            with pytest.raises(TypeError):
                dynamics += term

    def test_repr(self):
        gamma = 2.21e5
        self.precession = mm.Precession(gamma)
        alpha = 0.5
        dynamics = self.precession + self.damping

        exp_str = ("Precession(gamma=221000.0) + "
                   "Damping(alpha=0.5)")
        assert repr(dynamics) == exp_str

    def test_script(self):
        dynamics = mm.Dynamics()
        with pytest.raises(NotImplementedError):
            dynamics.script()

    def test_getattr(self):
        dynamics = self.precession + self.damping

        assert isinstance(dynamics.precession, mm.Precession)
        assert dynamics.precession.gamma == 2.21e5

        assert isinstance(dynamics.damping, mm.Damping)
        assert dynamics.damping.alpha == 0.5

    def test_getattr_error(self):
        dynamics = self.precession + self.damping

        with pytest.raises(AttributeError):
            stt = dynamics.stt

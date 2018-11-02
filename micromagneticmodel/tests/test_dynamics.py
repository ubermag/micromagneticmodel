import pytest
import micromagneticmodel as mm


class TestDynamics:
    def setup(self):
        gamma = 2.21e5
        self.precession = mm.Precession(gamma)
        alpha = 0.5
        self.damping = mm.Damping(alpha)
        u = (0, 0, 500)
        beta = 0.2
        self.stt = mm.STT(u=u, beta=beta)

        self.terms = [self.precession,
                      self.damping,
                      self.stt]

        self.invalid_terms = [1, 2.5, 0, 'abc', [3, 7e-12],
                              [self.precession, self.damping]]

    def test_add_terms(self):
        dynamics = mm.Dynamics()
        for term in self.terms:
            dynamics._add(term)
            assert isinstance(dynamics, mm.Dynamics)
            assert isinstance(dynamics.terms, list)
            assert dynamics.terms[-1] == term
            assert dynamics.terms[-1].name == term.name

        assert len(dynamics.terms) == 3

    def test_add_sum_of_terms(self):
        dynamics = self.precession + self.damping + self.stt

        assert isinstance(dynamics, mm.Dynamics)
        assert isinstance(dynamics.terms, list)
        assert len(dynamics.terms) == 3

    def test_add_dynamics(self):
        term_sum = self.precession + self.damping + self.stt
        dynamics = mm.Dynamics()
        dynamics += term_sum

        assert len(dynamics.terms) == 3

    def test_iadd(self):
        dynamics = mm.Dynamics()
        for term in self.terms:
            dynamics += term

            assert isinstance(dynamics, mm.Dynamics)
            assert isinstance(dynamics.terms, list)
            assert dynamics.terms[-1] == term
            assert dynamics.terms[-1].name == term.name

        assert len(dynamics.terms) == 3

    def test_repr_latex(self):
        dynamics = mm.Dynamics()
        latex = dynamics._repr_latex_()
        assert latex[0] == latex[-1] == '$'
        assert latex.count('$') == 2
        assert '\\frac' in latex
        assert latex[-2] == '0'

        for term in self.terms:
            dynamics._add(term)

        latex = dynamics._repr_latex_()

        assert latex[0] == latex[-1] == '$'
        assert latex.count('$') == 2
        assert r'-\gamma_{0}^{*}' in latex
        assert r'\mathbf{m}' in latex
        assert r'\mathbf{H}_\text{eff}' in latex
        assert r'\times' in latex
        assert r'\alpha' in latex
        assert latex.count('-') == 2
        assert latex.count('+') == 2
        assert latex.count('=') == 1
        assert latex.count(r'\partial') == 4

    def test_add_exception(self):
        dynamics = mm.Dynamics()
        for term in self.invalid_terms:
            with pytest.raises(TypeError):
                dynamics += term

    def test_repr(self):
        dynamics = self.precession + self.damping + self.stt

        exp_str = ('Precession(gamma=221000.0, name=\'precession\') + '
                   'Damping(alpha=0.5, name=\'damping\') + '
                   'STT(u=(0, 0, 500), beta=0.2, name=\'stt\')')
        assert repr(dynamics) == exp_str

    def test_getattr(self):
        dynamics = self.precession + self.damping + self.stt

        assert isinstance(dynamics.precession, mm.Precession)
        assert dynamics.precession.gamma == 2.21e5

        assert isinstance(dynamics.damping, mm.Damping)
        assert dynamics.damping.alpha == 0.5

        assert isinstance(dynamics.stt, mm.STT)
        assert dynamics.stt.u == (0, 0, 500)
        assert dynamics.stt.beta == 0.2

    def test_getattr_error(self):
        dynamics = self.precession + self.damping

        with pytest.raises(AttributeError):
            stt = dynamics.stt

    def test_script(self):
        dynamics = mm.Dynamics()
        with pytest.raises(NotImplementedError):
            script = dynamics._script

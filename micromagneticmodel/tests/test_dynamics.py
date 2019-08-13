import pytest
import micromagneticmodel as mm


class TestDynamics:
    def setup(self):
        gamma = 2.21e5
        self.precession = mm.Precession(gamma)
        alpha = {'r1': 1, 'r2': 0.5}
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
            dynamics += term
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

    def test_repr_latex(self):
        dynamics = mm.Dynamics()
        latex = dynamics._repr_latex_()
        assert isinstance(latex, str)

    def test_add_exception(self):
        dynamics = mm.Dynamics()
        for term in self.invalid_terms:
            with pytest.raises(TypeError):
                dynamics += term

    def test_repr(self):
        dynamics = self.precession + self.damping + self.stt
        assert isinstance(repr(dynamics), str)

    def test_getattr(self):
        dynamics = self.precession + self.damping + self.stt

        assert isinstance(dynamics.precession, mm.Precession)
        assert dynamics.precession.gamma == 2.21e5

        assert isinstance(dynamics.damping, mm.Damping)
        assert dynamics.damping.alpha == {'r1': 1, 'r2': 0.5}

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

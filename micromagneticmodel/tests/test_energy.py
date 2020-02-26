import pytest
import micromagneticmodel as mm
from .checks import check_container


class TestEnergy:
    def setup(self):
        self.exchange = mm.Exchange(A=1e-12)
        self.zeeman = mm.Zeeman(H=(0, 0, 1.2e6))
        self.uniaxialanisotropy = mm.UniaxialAnisotropy(K=1e4, u=(0, 1, 0))
        self.demag = mm.Demag()
        self.dmi = mm.DMI(D=1e-3, crystalclass='T')
        self.cubicanisotropy = mm.CubicAnisotropy(K={'r1': 1e6, 'r2': 5e6},
                                                  u1=(0, 0, 1),
                                                  u2=(0, 1, 0))

        self.terms = [self.exchange,
                      self.zeeman,
                      self.uniaxialanisotropy,
                      self.demag,
                      self.dmi,
                      self.cubicanisotropy]

        self.invalid_terms = [1, 2.5, 0, 'abc', [3, 7e-12],
                              [self.exchange, self.zeeman]]

    def test_init(self):
        container = mm.Energy(terms=self.terms)
        check_container(container)
        assert len(container) == 0

        container = mm.Energy()
        check_container(container)
        assert len(container) == 0

        for i, term in enumerate(self.terms):
            container += term
            check_container(container)
            assert len(container) == i + 1
            assert isinstance(container, mm.Energy)

        assert len(container) == 6

    def test_add_sum_of_terms(self):
        container = (self.exchange + self.zeeman + self.uniaxialanisotropy +
                     self.demag + self.dmi + self.cubicanisotropy)

        check_container(container)
        assert len(container) == 6

    def test_repr_latex(self):
        container = mm.Energy()
        check_container(container)
        latexstr = container._repr_latex_()
        assert latexstr == '$w=0$'

    def test_add_exception(self):
        container = mm.Energy()
        for term in self.invalid_terms:
            with pytest.raises(TypeError):
                container += term
    """
    def test_repr(self):
        container = self.exchange + self.zeeman + \
                      self.uniaxialanisotropy + self.demag + \
                      self.dmi + self.cubicanisotropy

        assert isinstance(repr(container), str)

    def test_getattr(self):
        container = mm.container()
        for term in self.terms:
            container += term

        assert isinstance(container.exchange, mm.Exchange)
        assert container.exchange.A == 1e-12

        assert isinstance(container.zeeman, mm.Zeeman)
        assert container.zeeman.H == (0, 0, 1.2e6)

        assert isinstance(container.uniaxialanisotropy,
                          mm.UniaxialAnisotropy)
        assert container.uniaxialanisotropy.K1 == 1e4
        assert container.uniaxialanisotropy.u == (0, 1, 0)

        assert isinstance(container.demag, mm.Demag)

        assert isinstance(container.cubicanisotropy,
                          mm.CubicAnisotropy)
        assert container.cubicanisotropy.K1 == {'r1': 1e6,
                                                  'r2': 5e6}
        assert container.cubicanisotropy.u1 == (0, 0, 1)
        assert container.cubicanisotropy.u2 == (0, 1, 0)

    def test_getattr_error(self):
        container = self.exchange + self.zeeman

        with pytest.raises(AttributeError):
            demag = container.demag

    def test_script(self):
        container = mm.container()
        with pytest.raises(NotImplementedError):
            script = container._script
    """

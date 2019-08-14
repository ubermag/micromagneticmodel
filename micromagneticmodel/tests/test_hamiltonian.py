import pytest
import micromagneticmodel as mm


class TestHamiltonian:
    def setup(self):
        A = 1e-12
        self.exchange = mm.Exchange(A=A)
        H = (0, 0, 1.2e6)
        self.zeeman = mm.Zeeman(H=H)
        K1 = 1e4
        K2 = {'r1': 1e6, 'r2': 5e6}
        u = (0, 1, 0)
        self.uniaxialanisotropy = mm.UniaxialAnisotropy(K1=K1, K2=K2, u=u)
        self.demag = mm.Demag()
        D = 1e-3
        crystalclass = 't'
        self.dmi = mm.DMI(D=D, crystalclass=crystalclass)
        K1 = {'r1': 1e6, 'r2': 5e6}
        u1 = (0, 0, 1)
        u2 = (0, 1, 0)
        self.cubicanisotropy = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)

        self.terms = [self.exchange,
                      self.zeeman,
                      self.uniaxialanisotropy,
                      self.demag,
                      self.dmi,
                      self.cubicanisotropy]

        self.invalid_terms = [1, 2.5, 0, 'abc', [3, 7e-12],
                              [self.exchange, self.zeeman]]

    def test_add_terms(self):
        hamiltonian = mm.Hamiltonian()
        for term in self.terms:
            hamiltonian += term

            assert isinstance(hamiltonian, mm.Hamiltonian)
            assert isinstance(hamiltonian.terms, list)
            assert hamiltonian.terms[-1] == term
            assert hamiltonian.terms[-1].name == term.name

        assert len(hamiltonian.terms) == 6

    def test_add_sum_of_terms(self):
        hamiltonian = self.exchange + self.zeeman + \
                      self.uniaxialanisotropy + self.demag + \
                      self.dmi + self.cubicanisotropy

        assert isinstance(hamiltonian, mm.Hamiltonian)
        assert isinstance(hamiltonian.terms, list)
        assert len(hamiltonian.terms) == 6

    def test_repr_latex(self):
        hamiltonian = mm.Hamiltonian()
        latex = hamiltonian._repr_latex_()
        assert isinstance(latex, str)
        hamiltonian = mm.Demag() + mm.Exchange(A=1e-12) + \
            mm.Zeeman(H=(0, 0, 1e6))
        latex = hamiltonian._repr_latex_()
        assert isinstance(latex, str)

    def test_add_exception(self):
        hamiltonian = mm.Hamiltonian()
        for term in self.invalid_terms:
            with pytest.raises(TypeError):
                hamiltonian += term

    def test_repr(self):
        hamiltonian = self.exchange + self.zeeman + \
                      self.uniaxialanisotropy + self.demag + \
                      self.dmi + self.cubicanisotropy

        assert isinstance(repr(hamiltonian), str)

    def test_getattr(self):
        hamiltonian = mm.Hamiltonian()
        for term in self.terms:
            hamiltonian += term

        assert isinstance(hamiltonian.exchange, mm.Exchange)
        assert hamiltonian.exchange.A == 1e-12

        assert isinstance(hamiltonian.zeeman, mm.Zeeman)
        assert hamiltonian.zeeman.H == (0, 0, 1.2e6)

        assert isinstance(hamiltonian.uniaxialanisotropy,
                          mm.UniaxialAnisotropy)
        assert hamiltonian.uniaxialanisotropy.K1 == 1e4
        assert hamiltonian.uniaxialanisotropy.u == (0, 1, 0)

        assert isinstance(hamiltonian.demag, mm.Demag)

        assert isinstance(hamiltonian.cubicanisotropy,
                          mm.CubicAnisotropy)
        assert hamiltonian.cubicanisotropy.K1 == {'r1': 1e6,
                                                  'r2': 5e6}
        assert hamiltonian.cubicanisotropy.u1 == (0, 0, 1)
        assert hamiltonian.cubicanisotropy.u2 == (0, 1, 0)

    def test_getattr_error(self):
        hamiltonian = self.exchange + self.zeeman

        with pytest.raises(AttributeError):
            demag = hamiltonian.demag

    def test_script(self):
        hamiltonian = mm.Hamiltonian()
        with pytest.raises(NotImplementedError):
            script = hamiltonian._script

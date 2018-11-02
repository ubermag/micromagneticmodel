import pytest
import micromagneticmodel as mm


class TestHamiltonian:
    def setup(self):
        A = 1e-12
        self.exchange = mm.Exchange(A=A)
        H = (0, 0, 1.2e6)
        self.zeeman = mm.Zeeman(H=H)
        K1 = 1e4
        K2 = 3e2
        u = (0, 1, 0)
        self.uniaxialanisotropy = mm.UniaxialAnisotropy(K1=K1, K2=K2, u=u)
        self.demag = mm.Demag()
        D = 1e-3
        crystalclass = 't'
        self.dmi = mm.DMI(D=D, crystalclass=crystalclass)
        K1 = 5e6
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
            hamiltonian._add(term)

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

    def test_add_hamiltonian(self):
        term_sum = self.exchange + self.zeeman
        hamiltonian = mm.Hamiltonian()
        hamiltonian += term_sum

        assert len(hamiltonian.terms) == 2

    def test_iadd(self):
        hamiltonian = mm.Hamiltonian()
        for term in self.terms:
            hamiltonian += term

            assert isinstance(hamiltonian, mm.Hamiltonian)
            assert isinstance(hamiltonian.terms, list)
            assert hamiltonian.terms[-1] == term
            assert hamiltonian.terms[-1].name == term.name

        assert len(hamiltonian.terms) == 6

    def test_repr_latex(self):
        hamiltonian = mm.Hamiltonian()
        latex = hamiltonian._repr_latex_()
        assert latex[0] == latex[-1] == '$'
        assert latex.count('$') == 2
        assert r'\mathcal{H}' in latex
        assert latex[-2] == '0'

        for term in self.terms:
            hamiltonian._add(term)

        latex = hamiltonian._repr_latex_()

        assert latex[0] == latex[-1] == '$'
        assert latex.count('$') == 2
        assert r'\mathcal{H}=' in latex
        assert 'A' in latex
        assert r'\mathbf{m}' in latex
        assert r'\mathbf{H}' in latex
        assert r'\mathbf{u}' in latex
        assert 'K' in latex
        assert r'\mathbf{H}_\text{d}' in latex
        assert '\cdot' in latex
        assert r'\frac{1}{2}' in latex
        assert r'M_\text{s}' in latex
        assert latex.count('-') == 5
        assert latex.count('+') == 3
        assert latex.count('=') == 1
        assert latex.count(r'\nabla') == 2
        assert latex.count(r'\times') == 1

    def test_add_exception(self):
        hamiltonian = mm.Hamiltonian()
        for term in self.invalid_terms:
            with pytest.raises(TypeError):
                hamiltonian += term

    def test_repr(self):
        hamiltonian = self.exchange + self.zeeman + \
                      self.uniaxialanisotropy + self.demag + \
                      self.dmi + self.cubicanisotropy

        exp_str = ('Exchange(A=1e-12, name=\'exchange\') + '
                   'Zeeman(H=(0, 0, 1200000.0), name=\'zeeman\') + '
                   'UniaxialAnisotropy(K1=10000.0, K2=300.0, u=(0, 1, 0), '
                   'name=\'uniaxialanisotropy\') + '
                   'Demag(name=\'demag\') + '
                   'DMI(D=0.001, crystalclass=\'t\', name=\'dmi\') + '
                   'CubicAnisotropy(K1=5000000.0, u1=(0, 0, 1), u2=(0, 1, 0), '
                   'name=\'cubicanisotropy\')')
        assert repr(hamiltonian) == exp_str

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
        assert hamiltonian.cubicanisotropy.K1 == 5e6
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

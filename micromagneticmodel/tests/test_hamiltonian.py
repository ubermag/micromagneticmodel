from micromagneticmodel.energies import ExchangeAbstract, \
    ZeemanAbstract, DemagAbstract, UniaxialAnisotropyAbstract, Hamiltonian


class Exchange(ExchangeAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        raise NotImplementedError()


class Demag(DemagAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        raise NotImplementedError()


class Zeeman(ZeemanAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        raise NotImplementedError()


class UniaxialAnisotropy(UniaxialAnisotropyAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        raise NotImplementedError()


class TestHamiltonian(object):
    def setup(self):
        A = 1e-12
        self.exchange = Exchange(A)
        H = (0, 0, 1.2e6)
        self.zeeman = Zeeman(H)
        K = 1e4
        u = (0, 1, 0)
        self.uniaxialanisotropy = UniaxialAnisotropy(K, u)
        self.demag = Demag()

        self.energies = [self.exchange,
                         self.zeeman,
                         self.uniaxialanisotropy,
                         self.demag]

    def test_add(self):
        hamiltonian = Hamiltonian()
        for energy in self.energies:
            hamiltonian.add(energy)

            assert isinstance(hamiltonian.energyterms, list)
            assert hamiltonian.energyterms[-1] == energy
            assert hamiltonian.energyterms[-1]._name == energy._name

        assert len(hamiltonian.energyterms) == 4

    def test_repr_latex(self):
        hamiltonian = Hamiltonian()
        for energy in self.energies:
            hamiltonian.add(energy)

        latex_str = hamiltonian._repr_latex_()

        assert '\\mathcal{H}=' in latex_str
        assert 'A' in latex_str
        assert '\mathbf{m}' in latex_str
        assert '\mathbf{H}' in latex_str
        assert '\mathbf{u}' in latex_str
        assert 'K' in latex_str
        assert '\mathbf{H}_\\text{d}' in latex_str
        assert '\cdot' in latex_str
        assert latex_str.count('-') == 2
        assert latex_str.count('+') == 3
        assert latex_str.count('=') == 1
        assert latex_str.count('\\nabla') == 3

        assert '\\frac{1}{2}' in latex_str
        assert 'M_\\text{s}' in latex_str

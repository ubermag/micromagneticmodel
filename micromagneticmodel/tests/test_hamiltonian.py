import pytest
from micromagneticmodel.energies import ExchangeAbstract, \
    ZeemanAbstract, DemagAbstract, UniaxialAnisotropyAbstract, Hamiltonian


class Exchange(ExchangeAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        return 'exchange_script\n'


class Demag(DemagAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        return 'demag_script\n'


class Zeeman(ZeemanAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        return 'zeeman_script\n'


class UniaxialAnisotropy(UniaxialAnisotropyAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        return 'uniaxialanisotropy_script\n'


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

        self.invalid_terms = [1, 2.5, 0, 'abc', [3, 7e-12],
                              [self.exchange, self.zeeman]]

    def test_add(self):
        hamiltonian = Hamiltonian()
        for energy in self.energies:
            hamiltonian.add(energy)

            assert isinstance(hamiltonian, Hamiltonian)
            assert isinstance(hamiltonian.energyterms, list)
            assert hamiltonian.energyterms[-1] == energy
            assert hamiltonian.energyterms[-1]._name == energy._name

        assert len(hamiltonian.energyterms) == 4

    def test_add(self):
        hamiltonian = self.exchange + self.zeeman + \
                      self.uniaxialanisotropy + self.demag

        assert isinstance(hamiltonian, Hamiltonian)
        assert isinstance(hamiltonian.energyterms, list)
        assert len(hamiltonian.energyterms) == 4

    def test_iadd(self):
        hamiltonian = Hamiltonian()
        for energy in self.energies:
            hamiltonian += energy

            assert isinstance(hamiltonian, Hamiltonian)
            assert isinstance(hamiltonian.energyterms, list)
            assert hamiltonian.energyterms[-1] == energy
            assert hamiltonian.energyterms[-1]._name == energy._name

        assert len(hamiltonian.energyterms) == 4

    def test_repr_latex(self):
        hamiltonian = Hamiltonian()
        latex_str = hamiltonian._repr_latex_()
        assert latex_str[0] == latex_str[-1] == '$'
        assert latex_str.count('$') == 2
        assert '\\mathcal{H}' in latex_str
        assert latex_str[-2] == '0'

        for energy in self.energies:
            hamiltonian.add(energy)

        latex_str = hamiltonian._repr_latex_()

        assert latex_str[0] == latex_str[-1] == '$'
        assert latex_str.count('$') == 2
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

    def test_add_exception(self):
        hamiltonian = Hamiltonian()
        for term in self.invalid_terms:
            with pytest.raises(TypeError):
                hamiltonian += term

    def test_calculator_script(self):
        hamiltonian = self.exchange + self.zeeman + \
                      self.uniaxialanisotropy + self.demag

        calculator_script = hamiltonian.calculator_script()

        assert isinstance(calculator_script, str)
        assert 'exchange_script' in calculator_script
        assert 'zeeman_script' in calculator_script
        assert 'demag_script' in calculator_script
        assert 'uniaxialanisotropy_script' in calculator_script
        assert calculator_script.count('\n') == 4

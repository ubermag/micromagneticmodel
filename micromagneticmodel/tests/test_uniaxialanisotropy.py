import pytest
import numpy as np
from numbers import Real
from micromagneticmodel.hamiltonian import UniaxialAnisotropy


class TestUniaxialAnisotropy(object):
    def setup(self):
        self.valid_args = [(1, (0, 1, 0)),
                           (5e6, [1, 1, 1]),
                           (-25.6e-3, np.array([0, 0, 1])),
                           (1.5, [1e6, 1e6, 5e9])]
        self.invalid_args = [('1', (0, 1, 0)),
                             (5e6, '(1, 1, 1)'),
                             (1e-3, (0, 0, 0, 1)),
                             (5, 5.0),
                             (-7e3, ('1', 2e6, 0)),
                             ((1, 0, 0), (0, 0, 1))]

    def test_init_valid_args(self):
        for arg in self.valid_args:
            K = arg[0]
            u = arg[1]
            anisotropy = UniaxialAnisotropy(K, u)

            assert anisotropy.K == K
            assert isinstance(anisotropy.K, Real)
            assert isinstance(anisotropy.u, (tuple, list, np.ndarray))
            assert len(u) == 3
            assert all([isinstance(i, Real) for i in anisotropy.u])

    def test_init_invalid_args(self):
        for arg in self.invalid_args:
            K = arg[0]
            u = arg[1]
            with pytest.raises(ValueError):
                anisotropy = UniaxialAnisotropy(K, u)

    def test_repr_latex(self):
        for arg in self.valid_args:
            K = arg[0]
            u = arg[1]
            anisotropy = UniaxialAnisotropy(K, u)
            latex_str = anisotropy._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex_str, str)
            assert latex_str[0] == latex_str[-1] == '$'
            assert 'K' in latex_str
            assert '\mathbf{u}' in latex_str
            assert '\mathbf{m}' in latex_str
            assert '^{2}' in latex_str
            assert '\cdot' in latex_str

    def test_name(self):
        for arg in self.valid_args:
            K = arg[0]
            u = arg[1]
            anisotropy = UniaxialAnisotropy(K, u)

            assert anisotropy._name == 'uniaxialanisotropy'

    def test_repr(self):
        for arg in self.valid_args:
            K = arg[0]
            u = arg[1]
            anisotropy = UniaxialAnisotropy(K, u)

            exp_str = "UniaxialAnisotropy(K={}, u={})".format(K, u)
            assert repr(anisotropy) == exp_str
            
        anisotropy = UniaxialAnisotropy(1000, (0, 0, 1))
        assert repr(anisotropy) == "UniaxialAnisotropy(K=1000, u=(0, 0, 1))"

    def test_script(self):
        for arg in self.valid_args:
            K = arg[0]
            u = arg[1]
            anisotropy = UniaxialAnisotropy(K, u)
            with pytest.raises(NotImplementedError):
                anisotropy.script()

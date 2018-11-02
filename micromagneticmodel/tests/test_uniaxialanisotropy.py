import pytest
import numbers
import numpy as np
import micromagneticmodel as mm


class TestUniaxialAnisotropy:
    def setup(self):
        self.valid_args = [(1, 5, (0, 1, 0)),
                           (5e6, 0, [1, 1, 1]),
                           (-25.6e-3, -2e-9, np.array([0, 0, 1])),
                           (1.5, 0, [1e6, 1e6, 5e9])]
        self.invalid_args = [('1', 5e6, (0, 1, 0)),
                             (5e6, 1e6, '(1, 1, 1)'),
                             (1e-3, 11, (0, 0, 0, 1)),
                             (5, 3.14, 5.0),
                             (-7e3, 2.7e4, ('1', 2e6, 0)),
                             ((1, 0, 0), 1e9, (0, 0, 1)),
                             (1, (5, 0), (0, 1, 0))]

    def test_init_valid_args(self):
        for K1, K2, u in self.valid_args:
            anisotropy = mm.UniaxialAnisotropy(K1=K1, K2=K2, u=u)
            assert anisotropy.K1 == K1
            assert anisotropy.K2 == K2
            assert isinstance(anisotropy.K1, numbers.Real)
            assert isinstance(anisotropy.K2, numbers.Real)
            assert isinstance(anisotropy.u, (tuple, list, np.ndarray))
            assert len(anisotropy.u) == 3
            assert all([isinstance(i, numbers.Real) for i in anisotropy.u])

    def test_init_invalid_args(self):
        for K1, K2, u in self.invalid_args:
            with pytest.raises(Exception):
                anisotropy = mm.UniaxialAnisotropy(K1=K1, K2=K2, u=u)

    def test_repr_latex(self):
        for K1, K2, u in self.valid_args:
            anisotropy = mm.UniaxialAnisotropy(K1=K1, K2=K2, u=u)
            latex = anisotropy._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex, str)
            assert latex[0] == latex[-1] == '$'
            assert 'K_{1}' in latex
            assert r'\mathbf{u}' in latex
            assert r'\mathbf{m}' in latex
            assert '^{2}' in latex
            assert r'\cdot' in latex
            if K2 != 0:
                assert 'K_{2}' in latex
                assert '^{4}' in latex

    def test_name(self):
        for K1, K2, u in self.valid_args:
            anisotropy = mm.UniaxialAnisotropy(K1=K1, K2=K2, u=u)
            assert anisotropy.name == 'uniaxialanisotropy'

    def test_repr(self):
        for K1, K2, u in self.valid_args:
            anisotropy = mm.UniaxialAnisotropy(K1=K1, K2=K2, u=u)
            exp_str = ('UniaxialAnisotropy(K1={}, K2={}, u={}, '
                       'name=\'{}\')').format(K1, K2, u, 'uniaxialanisotropy')
            assert repr(anisotropy) == exp_str

        anisotropy = mm.UniaxialAnisotropy(1000, (0, 0, 1), name='test_name')
        assert repr(anisotropy) == ('UniaxialAnisotropy(K1=1000, K2=0, '
                                    'u=(0, 0, 1), name=\'test_name\')')

    def test_script(self):
        for K1, K2, u in self.valid_args:
            anisotropy = mm.UniaxialAnisotropy(K1=K1, K2=K2, u=u)
            with pytest.raises(NotImplementedError):
                script = anisotropy._script

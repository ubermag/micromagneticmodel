import pytest
import numbers
import numpy as np
import micromagneticmodel as mm


class TestCubicAnisotropy:
    def setup(self):
        self.valid_args = [(1, (1, 0, 0), (0, 1, 0)),
                           (5e6, [1, 0, 1], [1, 1, 1]),
                           (-25.6e-3, (1, 0, 1), np.array([0, 0, -1])),
                           (1.5, [1e-6, 0, 0], [1e6, 1e6, 5e9])]
        self.invalid_args = [('1', (1, 0, 0), (0, 1, 0)),
                             (5e6, (-1, 0, -1), '(1, 1, 1)'),
                             (1e-3, (1, 0, 0), (0, 0, 0, 1)),
                             (5, (1, 0, 0), 5.0),
                             (-7e3, (0, 0, 1), ('1', 2e6, 0)),
                             ((1, 0, 0), (0, 0, 1), (0, 0, 1)),
                             (1, (5, 0), (0, 1, 0))]

    def test_init_valid_args(self):
        for K1, u1, u2 in self.valid_args:
            anisotropy = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)
            assert anisotropy.K1 == K1
            assert isinstance(anisotropy.K1, numbers.Real)
            assert isinstance(anisotropy.u1, (tuple, list, np.ndarray))
            assert isinstance(anisotropy.u2, (tuple, list, np.ndarray))
            assert len(anisotropy.u1) == 3
            assert len(anisotropy.u2) == 3
            assert all([isinstance(i, numbers.Real) for i in anisotropy.u1])
            assert all([isinstance(i, numbers.Real) for i in anisotropy.u2])

    def test_init_invalid_args(self):
        for K1, u1, u2 in self.invalid_args:
            with pytest.raises(Exception):
                anisotropy = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)

    def test_repr_latex(self):
        for K1, u1, u2 in self.valid_args:
            anisotropy = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)
            latex = anisotropy._repr_latex_()

            # Assert some characteristics of LaTeX string.
            assert isinstance(latex, str)
            assert latex[0] == latex[-1] == '$'
            assert 'K_{1}' in latex
            assert r'\mathbf{u}_{1}' in latex
            assert r'\mathbf{u}_{2}' in latex
            assert r'\mathbf{m}' in latex
            assert '^{2}' in latex
            assert r'\cdot' in latex
            assert latex.count(r'\mathbf{u}_{1}') == 2
            assert latex.count(r'\mathbf{u}_{2}') == 2
            assert latex.count(r'\mathbf{u}_{3}') == 2

    def test_name(self):
        for K1, u1, u2 in self.valid_args:
            anisotropy = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)
            assert anisotropy.name == 'cubicanisotropy'

    def test_repr(self):
        for K1, u1, u2 in self.valid_args:
            anisotropy = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)
            exp_str = ('CubicAnisotropy(K1={}, u1={}, u2={}, '
                       'name=\'{}\')').format(K1, u1, u2, 'cubicanisotropy')
            assert repr(anisotropy) == exp_str

        anisotropy = mm.CubicAnisotropy(1000, (0, 1, 0), (0, 0, 1),
                                        name='test_name')
        assert repr(anisotropy) == ('CubicAnisotropy(K1=1000, u1=(0, 1, 0), '
                                    'u2=(0, 0, 1), name=\'test_name\')')

    def test_script(self):
        for K1, u1, u2 in self.valid_args:
            anisotropy = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)
            with pytest.raises(NotImplementedError):
                script = anisotropy._script

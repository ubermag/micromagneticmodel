import pytest
import numbers
import numpy as np
import discretisedfield as df
import micromagneticmodel as mm


class TestCubicAnisotropy:
    def setup(self):
        self.valid_args = [(1, (1, 0, 0), (0, 1, 0)),
                           (5e6, (-1, 1, -1), [1, 1, 1]),
                           (-25.6e-3, (1, 0, 1), np.array([0, 0, 1])),
                           (1.5, (0, 0, 1), [1e6, 1e6, 5e9]),
                           ({'r1': 1e6, 'r2': 2e6},
                            (1, 0, 0), (0, 0, 1)),
                           (0, {'r1': (1, 0, 0), 'r2': (0, 0, 1)},
                            (0, 0, 1)),
                           (1e6, (0, 0, 1),
                            {'r1': (0, 0, 1), 'r2': (1, 0, 0)})]
        self.invalid_args = [('1', (1, 0, 0), (0, 1, 0)),
                             (5e6, 1e6, '(1, 1, 1)'),
                             (1e-3, (1, 0, 0), (0, 0, 0, 1)),
                             (5, 3.14, 5.0),
                             (-7e3, 2.7e4, ('1', 2e6, 0)),
                             ((1, 0, 0), 1e9, (0, 0, 1)),
                             (1, (5, 0), (0, 1, 0))]

    def test_init_valid_args(self):
        for K1, u1, u2 in self.valid_args:
            term = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)
            assert term.K1 == K1
            assert np.all(term.u1 == u1)
            assert np.all(term.u2 == u2)
            assert isinstance(term.u1, (tuple, list, np.ndarray, dict))
            assert isinstance(term.u2, (tuple, list, np.ndarray, dict))
            assert term.name == 'cubicanisotropy'

    def test_init_invalid_args(self):
        for K1, u1, u2 in self.invalid_args:
            with pytest.raises(Exception):
                term = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)

    def test_repr_latex_(self):
        for K1, u1, u2 in self.valid_args:
            term = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)
            assert isinstance(term._repr_latex_(), str)

    def test_repr(self):
        for K1, u1, u2 in self.valid_args:
            term = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)
            assert isinstance(repr(term), str)

    def test_script(self):
        for K1, u1, u2 in self.valid_args:
            term = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2)
            with pytest.raises(NotImplementedError):
                script = term._script

    def test_field(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=3, value=(0, 0, 1e6))
        term = mm.CubicAnisotropy(K1=field, u1=(1, 0, 0),
                                  u2=(0, 0, 1))
        assert isinstance(term.K1, df.Field)

    def test_kwargs(self):
        for K1, u1, u2 in self.valid_args:
            term = mm.CubicAnisotropy(K1=K1, u1=u1, u2=u2,
                                      e=1, something='a')
            assert term.e == 1
            assert term.something == 'a'

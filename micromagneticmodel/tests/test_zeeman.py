import pytest
import numbers
import numpy as np
import discretisedfield as df
import micromagneticmodel as mm


class TestZeeman:
    def setup(self):
        self.valid_args = [(1, 1.4, 1),
                           (0, 0, 1),
                           [1.2, 0, 0],
                           (0.56e6, 1.98e6, -1.1e7),
                           np.array([15e6, 0, 5e-8]),
                           {'r1': (0, 0, 0), 'r2': (4, 5, 6)}]
        self.invalid_args = [(1, 1),
                             1,
                             (1.2, 0, 0, 5),
                             (0.56, 1.98, '-1.1'),
                             ([15], [0], [np.pi]),
                             {'a': (0, 0, 0), 'b c': (0, 0, 1)}]

    def test_init_valid_args(self):
        for H in self.valid_args:
            term = mm.Zeeman(H=H)
            assert np.all(term.H == H)
            assert isinstance(term.H, (tuple, list, np.ndarray, dict))
            assert term.name == 'zeeman'

    def test_init_invalid_args(self):
        for H in self.invalid_args:
            with pytest.raises(Exception):
                term = mm.Zeeman(H=H)

    def test_repr_latex_(self):
        for H in self.valid_args:
            term = mm.Zeeman(H=H)
            assert isinstance(term._repr_latex_(), str)

    def test_repr(self):
        for H in self.valid_args:
            term = mm.Zeeman(H=H)
            assert isinstance(repr(term), str)

    def test_script(self):
        for H in self.valid_args:
            term = mm.Zeeman(H=H)
            with pytest.raises(NotImplementedError):
                script = term._script

    def test_field(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=3, value=(0, 0, 1e6))
        term = mm.Zeeman(H=field)
        assert isinstance(term.H, df.Field)

    def test_kwargs(self):
        for H in self.valid_args:
            term = mm.Zeeman(H=H, e=1, something='a')
            assert term.e == 1
            assert term.something == 'a'

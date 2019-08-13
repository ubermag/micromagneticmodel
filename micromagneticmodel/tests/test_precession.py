import pytest
import numbers
import discretisedfield as df
import micromagneticmodel as mm


class TestPrecession:
    def setup(self):
        self.valid_args = [1, 2.0, 5e-11, 1e6, {'a': 1, 'b': 1e-12}]
        self.invalid_args = [-1, -2.1, 'a', (1, 2), -3.6e-6, '0',
                             [1, 2, 3], {'a': -1, 'b': 3}]

    def test_init_valid_args(self):
        for gamma in self.valid_args:
            term = mm.Precession(gamma=gamma)
            assert term.gamma == gamma
            assert isinstance(term.gamma, (numbers.Real, dict))
            assert term.name == 'precession'

    def test_init_invalid_args(self):
        for gamma in self.invalid_args:
            with pytest.raises(Exception):
                term = mm.Precession(gamma=gamma)

    def test_repr_latex_(self):
        for gamma in self.valid_args:
            term = mm.Precession(gamma=gamma)
            assert isinstance(term._repr_latex_(), str)

    def test_repr(self):
        for gamma in self.valid_args:
            term = mm.Precession(gamma=gamma)
            assert isinstance(repr(term), str)

    def test_script(self):
        for gamma in self.valid_args:
            term = mm.Precession(gamma=gamma)
            with pytest.raises(NotImplementedError):
                script = term._script

    def test_field(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=1, value=1)
        term = mm.Precession(gamma=field)
        assert isinstance(term.gamma, df.Field)

    def test_kwargs(self):
        for gamma in self.valid_args:
            term = mm.Precession(gamma=gamma, e=1, something='a')
            assert term.e == 1
            assert term.something == 'a'

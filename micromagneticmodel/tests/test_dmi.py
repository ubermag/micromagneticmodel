import pytest
import numbers
import discretisedfield as df
import micromagneticmodel as mm


class TestDMI:
    def setup(self):
        self.valid_args = [1, 2.0, 5e-11, 1e6, {'a': 1, 'b': 1e-12}]
        self.invalid_args = ['a', (1, 2), {}, '0',
                             [1, 2, 3], {'a b': -1, 'b': 3}]

    def test_init_valid_args(self):
        for D in self.valid_args:
            term = mm.DMI(D=D, crystalclass='D2d')
            assert term.D == D
            assert isinstance(term.D, (numbers.Real, dict))
            assert term.name == 'dmi'

    def test_init_invalid_args(self):
        for D in self.invalid_args:
            with pytest.raises(Exception):
                term = mm.DMI(D=D, crystalclass='Cnv')

    def test_repr_latex_(self):
        for D in self.valid_args:
            term = mm.DMI(D=D, crystalclass='O')
            assert isinstance(term._repr_latex_(), str)
            term = mm.DMI(D=D, crystalclass='Cnv')
            assert isinstance(term._repr_latex_(), str)
            term = mm.DMI(D=D, crystalclass='D2d')
            assert isinstance(term._repr_latex_(), str)

    def test_repr(self):
        for D in self.valid_args:
            term = mm.DMI(D=D, crystalclass='T')
            assert isinstance(repr(term), str)

    def test_script(self):
        for D in self.valid_args:
            term = mm.DMI(D=D, crystalclass='Cnv')
            with pytest.raises(NotImplementedError):
                script = term._script

    def test_field(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=1, value=1)
        term = mm.DMI(D=field, crystalclass='D2d')
        assert isinstance(term.D, df.Field)

    def test_kwargs(self):
        for D in self.valid_args:
            term = mm.DMI(D=D, e=1, something='a')
            assert term.e == 1
            assert term.something == 'a'

import pytest
import numbers
import discretisedfield as df
import micromagneticmodel as mm


class TestExchange:
    def setup(self):
        self.valid_args = [1, 2.0, 5e-11, 1e6, {'a': 1, 'b': 1e-12}]
        self.invalid_args = [-1, -2.1, 'a', (1, 2), -3.6e-6, '0',
                             [1, 2, 3], {'a': -1, 'b': 3}]

    def test_init_valid_args(self):
        for A in self.valid_args:
            term = mm.Exchange(A=A)
            assert term.A == A
            assert isinstance(term.A, (numbers.Real, dict, df.Field))

        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=1, value=5)
        term = mm.Exchange(A=field)
        assert isinstance(term.A, df.Field)
        assert term.A.average == 5

    def test_init_invalid_args(self):
        for A in self.invalid_args:
            with pytest.raises(Exception):
                term = mm.Exchange(A=A)

    def test_repr_latex_(self):
        for A in self.valid_args:
            term = mm.Exchange(A=A)
            assert isinstance(term._repr_latex_(), str)

    def test_repr(self):
        for A in self.valid_args:
            term = mm.Exchange(A=A)
            assert isinstance(repr(term), str)

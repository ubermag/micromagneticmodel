import re
import pytest
import discretisedfield as df
import micromagneticmodel as mm
from .checks import check_term


class TestPrecession:
    def setup(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=1, value=5e-12)

        self.valid_args = [1, 2.0, 5e-11, 1e6, {'a': 1, 'b': 1e-12}, field]
        self.invalid_args = [-1, -2.1, 'a', (1, 2), -3.6e-6, '0',
                             [1, 2, 3], {'a': -1, 'b': 3}]

    def test_init_valid_args(self):
        for gamma in self.valid_args:
            term = mm.Precession(gamma=gamma)
            check_term(term)
            assert hasattr(term, 'gamma')
            assert term.name == 'precession'
            assert re.search(r'^Precession\(gamma=.+\)$', repr(term))

    def test_init_invalid_args(self):
        for gamma in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                term = mm.Precession(gamma=gamma)

        with pytest.raises(AttributeError):
            term = mm.Precession(wrong=1)

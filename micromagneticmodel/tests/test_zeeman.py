import re
import pytest
import numpy as np
import discretisedfield as df
import micromagneticmodel as mm
from .checks import check_term


class TestZeeman:
    def setup(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=3, value=(-1e5, 0, 1e6))

        self.valid_args = [(1, 1.4, 1),
                           (0, 0, 1),
                           [1.2, 0, 0],
                           (0.56e6, 1.98e6, -1.1e7),
                           np.array([15e6, 0, 5e-8]),
                           {'r1': (0, 0, 0), 'r2': (4, 5, 6)},
                           field]
        self.invalid_args = [(1, 1),
                             1,
                             (1.2, 0, 0, 5),
                             (0.56, 1.98, '-1.1'),
                             ([15], [0], [np.pi]),
                             {'a': (0, 0, 0), 'b c': (0, 0, 1)}]

    def test_init_valid_args(self):
        for H in self.valid_args:
            term = mm.Zeeman(H=H)
            check_term(term)
            assert hasattr(term, 'H')
            assert term.name == 'zeeman'
            assert re.search(r'^Zeeman\(H=.+\)$', repr(term))

    def test_init_invalid_args(self):
        for H in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                term = mm.Zeeman(H=H)

        with pytest.raises(AttributeError):
            term = mm.Zeeman(wrong=1)

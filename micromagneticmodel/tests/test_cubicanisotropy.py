import re

import discretisedfield as df
import numpy as np
import pytest

import micromagneticmodel as mm

from .checks import check_term


class TestCubicAnisotropy:
    def setup(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        Kfield = df.Field(mesh, dim=1, value=5e6)
        u1field = df.Field(mesh, dim=3, value=(1, 0, 0))
        u2field = df.Field(mesh, dim=3, value=(0, 1, 0))

        self.valid_args = [
            (1, (1, 0, 0), (0, 1, 0)),
            (5e6, (-1, 1, -1), [1, 1, 1]),
            (-25.6e-3, (1, 0, 1), np.array([0, 0, 1])),
            (1.5, (0, 0, 1), [1e6, 1e6, 5e9]),
            ({"r1": 1e6, "r2": 2e6}, (1, 0, 0), (0, 0, 1)),
            (0, {"r1": (1, 0, 0), "r2": (0, 0, 1)}, (0, 0, 1)),
            (1e6, (0, 0, 1), {"r1": (0, 0, 1), "r2": (1, 0, 0)}),
            (Kfield, u1field, u2field),
        ]
        self.invalid_args = [
            ("1", (1, 0, 0), (0, 1, 0)),
            (5e6, 1e6, "(1, 1, 1)"),
            (1e-3, (1, 0, 0), (0, 0, 0, 1)),
            (5, 3.14, 5.0),
            (-7e3, 2.7e4, ("1", 2e6, 0)),
            ((1, 0, 0), 1e9, (0, 0, 1)),
            (1, (5, 0), (0, 1, 0)),
        ]

    def test_init_valid_args(self):
        for K, u1, u2 in self.valid_args:
            term = mm.CubicAnisotropy(K=K, u1=u1, u2=u2)
            check_term(term)
            assert hasattr(term, "K")
            assert hasattr(term, "u1")
            assert hasattr(term, "u2")
            assert term.name == "cubicanisotropy"
            assert re.search(r"^CubicAnisotropy\(K=.+, u1=.+\, u2=.+\)$", repr(term))

    def test_init_invalid_args(self):
        for K, u1, u2 in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                mm.CubicAnisotropy(K=K, u1=u1, u2=u2)

        with pytest.raises(AttributeError):
            mm.CubicAnisotropy(wrong=1)

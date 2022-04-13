import re

import discretisedfield as df
import numpy as np
import pytest

import micromagneticmodel as mm

from .checks import check_term


class TestUniaxialAnisotropy:
    def setup(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        Kfield = df.Field(mesh, dim=1, value=5e6)
        ufield = df.Field(mesh, dim=3, value=(1, 0, 0))

        self.valid_args = [
            (1, (0, 1, 0)),
            (5e6, [1, 1, 1]),
            (-25.6e-3, np.array([0, 0, 1])),
            (1.5, [1e6, 1e6, 5e9]),
            ({"r1": 1e6, "r2": 2e6}, (0, 0, 1)),
            (3e6, (0, 0, 1)),
            (1e6, {"r1": (0, 0, 1), "r2": (1, 0, 0)}),
            (Kfield, ufield),
        ]
        self.invalid_args = [
            ("1", (0, 1, 0)),
            (5e6, "(1, 1, 1)"),
            (1e-3, (0, 0, 0, 1)),
            (5, 5.0),
            (-7e3, ("1", 2e6, 0)),
            ((1, 0, 0), (0, 0, 1)),
            ((5, 0), (0, 1, 0)),
        ]

    def test_init_valid_args(self):
        for K, u in self.valid_args:
            term = mm.UniaxialAnisotropy(K=K, u=u)
            check_term(term)
            assert hasattr(term, "K")
            assert hasattr(term, "u")
            assert term.name == "uniaxialanisotropy"
            assert re.search(r"^UniaxialAnisotropy\(K=.+, u=.+\)$", repr(term))

    def test_init_invalid_args(self):
        for K, u in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                mm.UniaxialAnisotropy(K=K, u=u)

        with pytest.raises(AttributeError):
            mm.UniaxialAnisotropy(wrong=1)

    def test_higher_order_anisotropy(self):
        term = mm.UniaxialAnisotropy(K1=1e5, K2=3e2, u=(0, 0, 1))
        check_term(term)

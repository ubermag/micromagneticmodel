import re

import discretisedfield as df
import pytest

import micromagneticmodel as mm

from .checks import check_term


class TestExchange:
    def setup(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=1, value=5e-12)

        self.valid_args = [1, 2.0, 5e-11, 1e6, {"a": 1, "b": 1e-12}, field]
        self.invalid_args = ["a", (1, 2), "0", [1, 2, 3], {"a": "c", "b": 3}]

    def test_init_valid_args(self):
        for A in self.valid_args:
            term = mm.Exchange(A=A)
            check_term(term)
            assert hasattr(term, "A")
            assert term.name == "exchange"
            assert re.search(r"^Exchange\(A=.+\)$", repr(term))

    def test_init_invalid_args(self):
        for A in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                mm.Exchange(A=A)

        with pytest.raises(AttributeError):
            mm.Exchange(wrong=1)

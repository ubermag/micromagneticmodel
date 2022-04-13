import re

import pytest

import micromagneticmodel as mm

from .checks import check_term


class TestRKKY:
    def setup(self):
        self.valid_args = [(1, ["a", "b"]), (-1, ["a", "bc"]), (0, ["r1", "r2"])]
        self.invalid_args = [("a", ["a", "b"]), (-1, "a"), (0, 0)]

    def test_init_valid_args(self):
        for sigma, subregions in self.valid_args:
            term = mm.RKKY(sigma=sigma, subregions=subregions)
            check_term(term)
            assert hasattr(term, "sigma")
            assert hasattr(term, "subregions")
            assert term.name == "rkky"
            assert re.search(r"^RKKY\(sigma=.+\)$", repr(term))

    def test_init_invalid_args(self):
        for sigma, subregions in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                mm.RKKY(sigma=sigma, subregions=subregions)

        with pytest.raises(AttributeError):
            mm.RKKY(wrong=1)

import re

import discretisedfield as df
import pytest

import micromagneticmodel as mm

from .checks import check_term


class TestDMI:
    def setup(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=1, value=5e-3)

        self.crystalclasses = [
            "T",
            "O",
            "Cnv_x",
            "Cnv_y",
            "Cnv_z",
            "D2d_x",
            "D2d_y",
            "D2d_z",
            "Cnv",
            "D2d",  # legacy crystalclass names
        ]
        self.valid_args = [1, 2.0, 5e-11, 1e6, {"a": 1, "b": 1e-12}, field]
        self.invalid_args = ["a", (1, 2), {}, "0", [1, 2, 3], {"a b": -1, "b": 3}]

    def test_init_valid_args(self):
        for crystalclass in self.crystalclasses:
            for D in self.valid_args:
                term = mm.DMI(D=D, crystalclass=crystalclass)
                check_term(term)
                assert hasattr(term, "D")
                assert hasattr(term, "crystalclass")
                assert term.name == "dmi"
                assert re.search(r"^DMI\(D=.+, crystalclass=\'\w+\'\)$", repr(term))

    def test_init_invalid_args(self):
        for crystalclass in self.crystalclasses:
            for D in self.invalid_args:
                with pytest.raises((TypeError, ValueError)):
                    mm.DMI(D=D, crystalclass=crystalclass)

        with pytest.raises(AttributeError):
            mm.DMI(wrong=1)

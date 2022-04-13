import re

import discretisedfield as df
import numpy as np
import pytest

import micromagneticmodel as mm

from .checks import check_term


class TestZeeman:
    def setup(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=3, value=(-1e5, 0, 1e6))

        self.valid_args = [
            (1, 1.4, 1),
            (0, 0, 1),
            [1.2, 0, 0],
            (0.56e6, 1.98e6, -1.1e7),
            np.array([15e6, 0, 5e-8]),
            {"r1": (0, 0, 0), "r2": (4, 5, 6)},
            field,
        ]
        self.invalid_args = [
            (1, 1),
            1,
            (1.2, 0, 0, 5),
            (0.56, 1.98, "-1.1"),
            ([15], [0], [np.pi]),
            {"a": (0, 0, 0), "b c": (0, 0, 1)},
        ]

    def test_init_valid_args(self):
        for H in self.valid_args:
            term = mm.Zeeman(H=H)
            check_term(term)
            assert hasattr(term, "H")
            assert term.name == "zeeman"
            assert re.search(r"^Zeeman\(H=.+\)$", repr(term))

    def test_init_invalid_args(self):
        for H in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                mm.Zeeman(H=H)

        with pytest.raises(AttributeError):
            mm.Zeeman(wrong=1)

    def test_init_time_dependent(self):
        for H in self.valid_args:
            # deprecated
            term = mm.Zeeman(H=H, wave="sin", f=1e9, t0=0)
            check_term(term)

            # deprecated
            term = mm.Zeeman(H=H, wave="sinc", f=1e9, t0=1e-12)
            check_term(term)

            term = mm.Zeeman(H=H, func="sin", f=1e9, t0=0)
            check_term(term)

            term = mm.Zeeman(H=H, func="sinc", f=1e9, t0=1e-12)
            check_term(term)

            def time_dep(t):
                return np.sin(t / 1e-10) ** 2

            term = mm.Zeeman(H=H, func=time_dep, dt=1e-12)
            check_term(term)

            tcl_strings = {}
            tcl_strings[
                "script"
            ] = """proc TimeFunction { total_time } {
            set PI [expr {4*atan(1.)}]
            set w [expr {1e9*2*$PI}]
            set ct [expr {cos($w*$total_time)}]
            set mct [expr {-1*$ct}]      ;# "mct" is "minus cosine (w)t"
            set st [expr {sin($w*$total_time)}]
            set mst [expr {-1*$st}]      ;# "mst" is "minus sine (w)t"
            return [list  $ct $mst  0 \
                            $st $ct   0 \
                            0   0   1 \
                            [expr {$w*$mst}] [expr {$w*$mct}] 0 \
                            [expr {$w*$ct}]  [expr {$w*$mst}] 0 \
                                0                0         0]
            }"""
            tcl_strings["energy"] = "Oxs_TransformZeeman"
            tcl_strings["type"] = "general"
            tcl_strings["script_args"] = "total_time"
            tcl_strings["script_name"] = "TimeFunction"

            term = mm.Zeeman(H=H, tcl_strings=tcl_strings)
            check_term(term)

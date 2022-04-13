import re

import numpy as np
import pytest

import micromagneticmodel as mm

from .checks import check_term


class TestZhangLi:
    def setup(self):
        self.valid_args = [
            (1, 1),
            (-1.0, 2.0),
            (0, 5e-11),
            (19, -1e-12),
            ({"r1": 1, "r2": 2}, 0.5),
        ]
        self.invalid_args = [
            ((1, -2), 1),
            (-1.0, "2.0"),
            ((0, 0, 0, 9), 5e-11),
            (11, -1e-12 + 2j),
            (1, {"r1 2": 1, "r2": 2}),
        ]

    def test_init_valid_args(self):
        for u, beta in self.valid_args:
            term = mm.ZhangLi(u=u, beta=beta)
            check_term(term)
            assert hasattr(term, "u")
            assert hasattr(term, "beta")
            assert term.name == "zhangli"
            assert re.search(r"^ZhangLi\(u=.+\, beta=.+\)$", repr(term))

    def test_init_invalid_args(self):
        for u, beta in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                mm.ZhangLi(u=u, beta=beta)

        with pytest.raises(AttributeError):
            mm.ZhangLi(wrong=1)

    def test_init_time_dependent(self):
        def time_dep(t):
            return np.sin(t / 1e-10) ** 2

        for u, beta in self.valid_args:
            term = mm.ZhangLi(u=u, beta=beta, func=time_dep, dt=1e-12)
            check_term(term)
            assert hasattr(term, "u")
            assert hasattr(term, "beta")
            assert hasattr(term, "func")
            assert hasattr(term, "dt")
            assert term.name == "zhangli"
            assert re.search(r"^ZhangLi\(u=.+\, beta=.+\)$", repr(term))

            tcl_strings = {}
            tcl_strings[
                "script"
            ] = """proc TimeFunction { total_time } {
            return $total_time/10
            }"""
            tcl_strings["script_args"] = "total_time"
            tcl_strings["script_name"] = "TimeFunction"

            term = mm.ZhangLi(u=u, beta=beta, tcl_strings=tcl_strings)
            check_term(term)
            assert hasattr(term, "u")
            assert hasattr(term, "beta")
            assert hasattr(term, "tcl_strings")
            assert term.name == "zhangli"
            assert re.search(r"^ZhangLi\(u=.+\, beta=.+\)$", repr(term))

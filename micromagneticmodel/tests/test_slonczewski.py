import re

import discretisedfield as df
import numpy as np
import pytest

import micromagneticmodel as mm

from .checks import check_term


class TestSlonczewski:
    def setup(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=1, value=5e-12)

        self.valid_args = [
            (1e12, (0, 0, 1), 0.2, 3, 0),
            (5e12, [0, 1, 0], 0.4, 2, 1),
            (5e12, [0, 1, 0], {"r1": 0.4, "r2": 0.3}, 2, 1),
            (field, [0, 1, 0], 0.4, 2, 1),
        ]
        self.invalid_args = [
            (1e12, 2, 0.2, 3, 0),
            (5e12, [0, 1, 0, 1], 0.4, 2, 1),
            ((0, 0), [0, 1, 0], {"r1": 0.4, "r2": 0.3}, 2, 1),
            (field, [0, 1, 0], 0.4, 2, (0, 0, 1)),
        ]

    def test_init_valid_args(self):
        for J, mp, P, Lambda, eps_prime in self.valid_args:
            term = mm.Slonczewski(J=J, mp=mp, P=P, Lambda=Lambda, eps_prime=eps_prime)
            check_term(term)
            assert hasattr(term, "J")
            assert term.name == "slonczewski"
            assert re.search(r"^Slonczewski\(J=.+\)$", repr(term))

            if not eps_prime:
                assert "'" not in term._repr_latex_()
            else:
                assert "'" in term._repr_latex_()

    def test_init_invalid_args(self):
        for J, mp, P, Lambda, eps_prime in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                mm.Slonczewski(J=J, mp=mp, P=P, Lambda=Lambda, eps_prime=eps_prime)

        with pytest.raises(AttributeError):
            mm.Slonczewski(wrong=1)

    def test_init_time_dependent(self):
        def time_dep(t):
            return np.sin(t / 1e-10) ** 2

        for J, mp, P, Lambda, eps_prime in self.valid_args:
            term = mm.Slonczewski(
                J=J,
                mp=mp,
                P=P,
                Lambda=Lambda,
                eps_prime=eps_prime,
                func=time_dep,
                dt=1e-12,
            )
            check_term(term)
            assert hasattr(term, "J")
            assert hasattr(term, "func")
            assert hasattr(term, "dt")
            assert term.name == "slonczewski"
            assert re.search(r"^Slonczewski\(J=.+\)$", repr(term))

            tcl_strings = {}
            tcl_strings[
                "script"
            ] = """proc TimeFunction { total_time } {
            return $total_time/10
            }"""
            tcl_strings["script_args"] = "total_time"
            tcl_strings["script_name"] = "TimeFunction"

            term = mm.Slonczewski(
                J=J,
                mp=mp,
                P=P,
                Lambda=Lambda,
                eps_prime=eps_prime,
                tcl_strings=tcl_strings,
            )
            check_term(term)
            assert hasattr(term, "J")
            assert hasattr(term, "tcl_strings")
            assert term.name == "slonczewski"
            assert re.search(r"^Slonczewski\(J=.+\)$", repr(term))

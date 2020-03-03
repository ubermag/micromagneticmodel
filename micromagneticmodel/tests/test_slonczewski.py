import re
import pytest
import discretisedfield as df
import micromagneticmodel as mm
from .checks import check_term


class TestSlonczewski:
    def setup(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=1, value=5e-12)

        self.valid_args = [(1e12, (0, 0, 1), 0.2, 3, 0),
                           (5e12, [0, 1, 0], 0.4, 2, 1),
                           (5e12, [0, 1, 0], {'r1': 0.4, 'r2': 0.3}, 2, 1),
                           (field, [0, 1, 0], 0.4, 2, 1)]
        self.invalid_args = [(1e12, 2, 0.2, 3, 0),
                             (5e12, [0, 1, 0, 1], 0.4, 2, 1),
                             ((0, 0), [0, 1, 0], {'r1': 0.4, 'r2': 0.3}, 2, 1),
                             (field, [0, 1, 0], 0.4, 2, (0, 0, 1))]

    def test_init_valid_args(self):
        for J, mp, P, Lambda, eps_prime in self.valid_args:
            term = mm.Slonczewski(J=J, mp=mp, P=P, Lambda=Lambda,
                                  eps_prime=eps_prime)
            check_term(term)
            assert hasattr(term, 'J')
            assert term.name == 'slonczewski'
            assert re.search(r'^Slonczewski\(J=.+\)$', repr(term))

            if not eps_prime:
                assert "'" not in term._repr_latex_()
            else:
                assert "'" in term._repr_latex_()

    def test_init_invalid_args(self):
        for J, mp, P, Lambda, eps_prime in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                term = mm.Slonczewski(J=J, mp=mp, P=P, Lambda=Lambda,
                                      eps_prime=eps_prime)

        with pytest.raises(AttributeError):
            term = mm.Slonczewski(wrong=1)

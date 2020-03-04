import re
import pytest
import discretisedfield as df
import micromagneticmodel as mm
from .checks import check_term


class TestZhangLi:
    def setup(self):
        self.valid_args = [(1, 1),
                           (-1.0, 2.0),
                           (0, 5e-11),
                           (19, -1e-12),
                           ({'r1': 1, 'r2': 2}, 0.5)]
        self.invalid_args = [((1, -2), 1),
                             (-1.0, '2.0'),
                             ((0, 0, 0, 9), 5e-11),
                             (11, -1e-12+2j),
                             (1, {'r1 2': 1, 'r2': 2})]

    def test_init_valid_args(self):
        for u, beta in self.valid_args:
            term = mm.ZhangLi(u=u, beta=beta)
            check_term(term)
            assert hasattr(term, 'u')
            assert hasattr(term, 'beta')
            assert term.name == 'zhangli'
            assert re.search(r'^ZhangLi\(u=.+\, beta=.+\)$', repr(term))

    def test_init_invalid_args(self):
        for u, beta in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                term = mm.ZhangLi(u=u, beta=beta)

        with pytest.raises(AttributeError):
            term = mm.ZhangLi(wrong=1)

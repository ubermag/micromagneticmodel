from micromagneticmodel.consts import mu0
from math import pi


def test_mu0():
    assert mu0 == 4 * pi * 1e-7  # magnetic constant (N/A**2)

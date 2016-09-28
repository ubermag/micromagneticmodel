import numpy as np
from micromagneticmodel.consts import mu0


def test_mu0():
    assert mu0 == 4*np.pi*1e-7  # magnetic constant (N/A**2)

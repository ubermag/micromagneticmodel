import numpy as np
import micromagneticmodel.consts as mcc


class TestConsts:
    def test_mu0(self):
        assert mcc.mu0 == 4*np.pi*1e-7  # magnetic constant (N/A**2)

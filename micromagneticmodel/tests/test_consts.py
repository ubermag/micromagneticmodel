import importlib
import numpy as np
import micromagneticmodel as mm


class TestConsts:
    def test_mu0(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert self.selfmodule.mu0 == 4*np.pi*1e-7

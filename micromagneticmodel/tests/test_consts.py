import importlib
import numpy as np
import micromagneticmodel as mm


class TestConsts:
    def test_mu0(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert self.selfmodule.mu0 == 4*np.pi*1e-7

    def test_e(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert self.selfmodule.e == 1.6021766208e-19

    def test_muB(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert self.selfmodule.muB == 9.27400968e-24

    def test_kB(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert self.selfmodule.kB == 1.38064852e-23

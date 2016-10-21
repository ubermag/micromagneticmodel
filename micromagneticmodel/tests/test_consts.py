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

    def test_me(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert self.selfmodule.me == 9.1093835611e-31

    def test_kB(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert self.selfmodule.kB == 1.3806485279e-23

    def test_h(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert self.selfmodule.h == 6.62607004081e-34

    def test_g(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert self.selfmodule.g == 2.00231930436182

    def test_hbar(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert abs(self.selfmodule.hbar - 1.05457180013e-34) < 1e-40

    def test_gamma(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert abs(self.selfmodule.gamma - 176085964286.56906) < 1e-3

    def test_muB(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert abs(self.selfmodule.muB == 9.27400968e-24) < 1e-30

    def test_gamma0(self):
        self.selfmodule = importlib.__import__(self.__class__.__module__)
        assert abs(self.selfmodule.gamma0 - 2.2127614872e5) < 1e-3

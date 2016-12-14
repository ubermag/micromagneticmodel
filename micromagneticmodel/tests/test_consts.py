import importlib
import numpy as np
import micromagneticmodel as mm


class TestConsts:
    def test_mu0(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert self.module.mu0 == 4*np.pi*1e-7

    def test_e(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert self.module.e == 1.6021766208e-19

    def test_me(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert self.module.me == 9.1093835611e-31

    def test_kB(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert self.module.kB == 1.3806485279e-23

    def test_h(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert self.module.h == 6.62607004081e-34

    def test_g(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert self.module.g == 2.00231930436182

    def test_hbar(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert abs(self.module.hbar - 1.05457180013e-34) < 1e-40

    def test_gamma(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert abs(self.module.gamma - 176085964286.56906) < 1e-3

    def test_muB(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert abs(self.module.muB == 9.27400968e-24) < 1e-30

    def test_gamma0(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert abs(self.module.gamma0 - 2.2127614872e5) < 1e-3

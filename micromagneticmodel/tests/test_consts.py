import importlib

class TestConsts:
    def test_consts(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert hasattr(self.module, 'mu0')
        assert hasattr(self.module, 'e')
        assert hasattr(self.module, 'me')
        assert hasattr(self.module, 'kB')
        assert hasattr(self.module, 'h')
        assert hasattr(self.module, 'g')
        assert hasattr(self.module, 'hbar')
        assert hasattr(self.module, 'gamma')
        assert hasattr(self.module, 'muB')
        assert hasattr(self.module, 'gamma0')

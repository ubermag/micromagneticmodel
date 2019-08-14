import importlib


class TestConsts:
    def test_consts(self):
        self.module = importlib.__import__(self.__class__.__module__)
        assert hasattr(self.module.consts, 'mu0')
        assert hasattr(self.module.consts, 'e')
        assert hasattr(self.module.consts, 'me')
        assert hasattr(self.module.consts, 'kB')
        assert hasattr(self.module.consts, 'h')
        assert hasattr(self.module.consts, 'g')
        assert hasattr(self.module.consts, 'hbar')
        assert hasattr(self.module.consts, 'gamma')
        assert hasattr(self.module.consts, 'muB')
        assert hasattr(self.module.consts, 'gamma0')

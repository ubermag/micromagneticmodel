import pytest
from micromagneticmodel.drivers import MinDriver


class TestMinDriver:
    def setup(self):
        self.md = MinDriver(None)

    def test_drive(self):
        with pytest.raises(NotImplementedError):
            self.md.drive()

    def test_script(self):
        with pytest.raises(NotImplementedError):
            self.md.script()

    def test_run_simulator(self):
        with pytest.raises(NotImplementedError):
            self.md.run_simulator()

    def test_update_system(self):
        with pytest.raises(NotImplementedError):
            self.md.update_system()

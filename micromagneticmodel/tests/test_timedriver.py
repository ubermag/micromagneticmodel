import pytest
from micromagneticmodel.drivers import TimeDriver

class TestTimeDriver:
    def setup(self):
        self.td = TimeDriver(None)

    def test_drive(self):
        with pytest.raises(NotImplementedError):
            self.td.drive()

    def test_script(self):
        with pytest.raises(NotImplementedError):
            self.td.script()

    def test_run_simulator(self):
        with pytest.raises(NotImplementedError):
            self.td.run_simulator()

    def test_update_system(self):
        with pytest.raises(NotImplementedError):
            self.td.update_system()

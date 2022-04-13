import micromagneticmodel as mm


class MyDriver(mm.Driver):
    _allowed_attributes = ["arg1", "arg2"]

    def drive(self, system):  # A simple drive method
        return system


class TestDriver:
    def test_drive(self):
        driver = MyDriver()
        assert driver.drive(system=5) == 5

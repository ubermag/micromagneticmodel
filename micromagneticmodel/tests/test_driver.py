import discretisedfield as df
import pytest

import micromagneticmodel as mm


class MyDriver(mm.Driver):
    _allowed_attributes = ["arg1", "arg2"]

    def drive(self, system):  # A simple drive method
        return system

    @property
    def _x(self):
        return "independent_variable"


class MyExternalDriver(mm.ExternalDriver):
    _allowed_attributes = ["arg1", "arg2"]

    @property
    def _x(self):
        return "x"

    def schedule_kwargs_setup(self, **kwargs):
        pass

    def drive_kwargs_setup(self, **kwargs):
        pass

    def _write_input_files(self, system, **kwargs):
        with open(f"{system.name}.input", "wt", encoding="utf-8") as f:
            f.write(str(-1))  # factor -1 used to invert magnetisation direction in call
        self._write_info_json(system, **kwargs)

    def _call(self, system, runner, dry_run=False, **kwargs):
        if dry_run:
            # Python is used to test/simulate schedule during tests because there
            # typically is no scheduling system and Python is always available.
            # Therefore, dry_run must return a Python comment that can be added to the
            # schedule script without breaking the execution.
            return ["#", "run", "command", "line"]
        with open(f"{system.name}.input", "rt", encoding="utf-8") as f:
            factor = int(f.read())
        (factor * system.m).write("output.omf")

    def _read_data(self, system):
        system.m = df.Field.fromfile("output.omf")


def test_driver():
    driver = MyDriver()
    assert driver.drive(system=5) == 5
    assert driver._x == "independent_variable"


def test_external_driver(tmp_path):
    system = mm.examples.macrospin()
    driver = MyExternalDriver(arg1="a", arg2="b")
    assert driver._x == "x"

    driver.drive(system, dirname=str(tmp_path))
    m_out = df.Field.fromfile(str(tmp_path / system.name / "drive-0" / "output.omf"))
    assert system.m.allclose(m_out)
    assert system.m.allclose(-mm.examples.macrospin().m)
    assert (tmp_path / system.name / "drive-0" / "info.json").exists()

    with pytest.raises(FileExistsError):
        driver.drive(system, dirname=str(tmp_path), append=False)

    # There is no scheduling system available for the tests. Instead we use 'python'
    # because we know that this is always an executable. The created schedule script
    # contains only Python comments so nothing is actually happening.
    driver.schedule(system, "python", "#Schedule header", dirname=str(tmp_path))
    assert (tmp_path / system.name / "drive-1" / "macrospin.input").exists()
    assert (tmp_path / system.name / "drive-1" / "info.json").exists()
    assert (tmp_path / system.name / "drive-1" / "job.sh").exists()

    # Schedule header from file and runtime error during schedule.
    with (tmp_path / "header.sh").open("wt", encoding="utf-8") as f:
        f.write("import sys\nsys.exit(1)")
    with pytest.raises(RuntimeError):
        driver.schedule(
            system, "python", str(tmp_path / "header.sh"), dirname=str(tmp_path)
        )
        assert (tmp_path / system.name / "drive-2" / "macrospin.input").exists()
        assert (tmp_path / system.name / "drive-2" / "info.json").exists()
        assert (tmp_path / system.name / "drive-2" / "job.sh").exists()

    assert len(list((tmp_path / system.name).glob("drive*"))) == 3

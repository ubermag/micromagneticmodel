import json

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

    def schedule_kwargs_setup(self, schedule_kwargs):
        pass

    def drive_kwargs_setup(self, drive_kwargs):
        pass

    def _check_system(self, system):
        pass

    def _write_input_files(self, system, **kwargs):
        with open(f"{system.name}.input", "w", encoding="utf-8") as f:
            f.write(str(-1))  # factor -1 used to invert magnetisation direction in call

    def _call(self, system, runner, **kwargs):
        with open(f"{system.name}.input", encoding="utf-8") as f:
            factor = int(f.read())
        (factor * system.m).to_file("output.omf")

    def _schedule_commands(self, system, runner):
        # Python is used to test/simulate schedule during tests because there
        # typically is no scheduling system and Python is always available.
        # Therefore, we return a Python comment that can be added to the
        # schedule script without breaking the execution.
        return ["# run command line"]

    def _read_data(self, system):
        system.m = df.Field.from_file("output.omf")


def test_driver():
    driver = MyDriver()
    assert driver.drive(system=5) == 5
    assert driver._x == "independent_variable"


def test_external_driver(tmp_path):
    system = mm.examples.macrospin()
    driver = MyExternalDriver(arg1="a", arg2="b")
    assert driver._x == "x"

    driver.drive(system, dirname=str(tmp_path))
    m_out = df.Field.from_file(tmp_path / system.name / "drive-0" / "output.omf")
    assert system.m.allclose(m_out)
    assert system.m.allclose(-mm.examples.macrospin().m)
    assert (tmp_path / system.name / "drive-0" / "info.json").exists()

    with open(tmp_path / system.name / "drive-0" / "info.json") as f:
        info = json.load(f)

    assert info["adapter"] == "micromagneticmodel"
    assert info["driver"] == "MyExternalDriver"
    assert info["drive_number"] == 0

    assert "start_time" in info
    assert "end_time" in info
    assert "elapsed_time" in info
    assert "success" in info
    assert info["success"]

    def _parse_time_str_to_seconds(time_str):
        h, m, s = map(int, time_str.split(":"))
        return h * 3600 + m * 60 + s

    elapsed_time = info["elapsed_time"]
    elapsed_seconds = _parse_time_str_to_seconds(elapsed_time)
    # assumption: this test runs in under one minute
    assert elapsed_seconds < 60

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

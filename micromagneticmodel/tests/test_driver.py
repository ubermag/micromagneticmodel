import json

import discretisedfield as df
import pytest

import micromagneticmodel as mm
from micromagneticmodel import adapter_base


class MyDriver(adapter_base.Driver):
    _allowed_attributes = ["arg1", "arg2"]

    def drive(self, system):  # A simple drive method
        return system

    @property
    def _x(self):
        return "independent_variable"


def test_driver():
    # The `Driver` base class imposes no restrictions on anything and only defines
    # the `drive` method as public API. It needs to take a `system` (but does not
    # enforce any checks on it) and should return the updated system.
    # For simplicity, the `MyDriver` implementation just returns the system passed in
    # so we can use an integer
    driver = MyDriver()
    assert driver.drive(system=5) == 5
    assert driver._x == "independent_variable"


class MyExternalDriver(adapter_base.ExternalDriver):
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


def test_external_driver(tmp_path):
    # This test contains multiple invocations of drive/schedule so that we can test
    # the creation of multiple drive directories in the same system directory
    system = mm.examples.macrospin()
    driver = MyExternalDriver(arg1="a", arg2="b")
    assert driver._x == "x"

    # == first invocation ==
    # check input and output files
    driver.drive(system, dirname=tmp_path)
    m_out = df.Field.from_file(tmp_path / system.name / "drive-0" / "output.omf")
    assert system.m.allclose(m_out)
    # MyExternalDriver inverts magnetisation in every call to drive
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
    # we round to full seconds, so it should be > 0
    assert 0 < elapsed_seconds < 60

    # == second invocation ==
    # calling drive with append=False fails if the system directory exists already
    with pytest.raises(FileExistsError):
        driver.drive(system, dirname=str(tmp_path), append=False)

    # == third invocation ==
    # There is no scheduling system available for the tests, instead we use 'python'.
    # The created schedule script contains only Python comments so nothing is actually
    # happening.
    driver.schedule(system, "python", "#Schedule header", dirname=str(tmp_path))
    assert (tmp_path / system.name / "drive-1" / "macrospin.input").exists()
    assert (tmp_path / system.name / "drive-1" / "info.json").exists()
    assert (tmp_path / system.name / "drive-1" / "job.sh").exists()
    # the simulation is never executed, so no output can exist
    assert not (tmp_path / system.name / "drive-1" / "output.omf").exists()
    # scheduling does not update the system, so we still have the state of the first run
    assert system.m.allclose(-mm.examples.macrospin().m)

    # == fourth invocation ==
    # Schedule header from file
    with (tmp_path / "header.sh").open("wt", encoding="utf-8") as f:
        f.write("import sys\nsys.exit(1)")
    with pytest.raises(RuntimeError):
        # the schedule header calls `exit(1)`, meaning the scheduling fails
        driver.schedule(
            system, "python", str(tmp_path / "header.sh"), dirname=str(tmp_path)
        )
    # despite the failed scheduling, the input files have been written
    assert (tmp_path / system.name / "drive-2" / "macrospin.input").exists()
    assert (tmp_path / system.name / "drive-2" / "info.json").exists()
    assert (tmp_path / system.name / "drive-2" / "job.sh").exists()

    assert len(list((tmp_path / system.name).glob("drive*"))) == 3

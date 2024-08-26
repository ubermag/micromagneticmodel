import subprocess as sp

import pytest

import micromagneticmodel as mm


class MyRunner(mm.ExternalRunner):
    @property
    def package_name(self):
        return "my_package"

    def _call(self, argstr, need_stderr=False, dry_run=False, returncode=0, **kwargs):
        if dry_run:
            return ["my_package", argstr, "command", "line"]
        return sp.CompletedProcess(
            argstr,
            returncode=returncode,
            stdout=b"output",
            stderr=b"error",
        )


def test_call(capsys):
    runner = MyRunner()
    command = runner._call("argstr", dry_run=True)
    assert command == ["my_package", "argstr", "command", "line"]

    runner.call("argstr")
    captured = capsys.readouterr()
    assert "Running my_package" in captured.out
    assert captured.err == ""

    runner.call("argstr", verbose=0)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

    runner.call("argstr", verbose=2)  # no total -> output like verbose=1
    captured = capsys.readouterr()
    assert "Running my_package" in captured.out
    assert captured.err == ""

    with pytest.raises(RuntimeError):
        runner.call("argstr", returncode=1)

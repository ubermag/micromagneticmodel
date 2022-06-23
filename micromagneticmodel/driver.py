import abc
import datetime
import json
import pathlib
import subprocess as sp
import sys

import ubermagutil as uu

import micromagneticmodel as mm


class Driver(mm.abstract.Abstract):
    """An abstract class for deriving drivers."""

    @abc.abstractmethod
    def drive(self, system, **kwargs):
        """Drives the system in phase space."""

    @property
    @abc.abstractmethod
    def _x(self):
        """Independent variable."""


class ExternalDriver(Driver):
    """Base class for existing external simulation packages (e.g. OOMMF, mumax3)."""

    @abc.abstractmethod
    def drive_kwargs_setup(self, **kwargs):
        """Abstract method to check and initialise kwargs for drive."""

    @abc.abstractmethod
    def schedule_kwargs_setup(self, **kwargs):
        """Abstract method to check and initialise kwargs for schedule."""

    @abc.abstractmethod
    def _write_input_files(system, **kwargs):
        """Write input files required for the external package."""

    @abc.abstractmethod
    def _call(self, system, runner, dry_run=False, **kwargs):
        """Call the external package."""

    @abc.abstractmethod
    def _read_data(self, system):
        """Update system with simulation output (magnetisation and scalar data)."""

    def drive(
        self,
        system,
        /,
        dirname=".",
        append=True,
        runner=None,
        ovf_format="bin8",
        verbose=1,
        **kwargs,
    ):
        """Drives the system in phase space.

        Takes ``micromagneticmodel.System`` and drives it in phase space. If
        ``append=True`` and the system director already exists, drive will be appended
        to that directory. Otherwise, an exception will be raised.

        This method accepts any other arguments that could be required by the specific
        driver. Refer to ``drive_kwargs_setup`` of the derived class for details.

        Parameters
        ----------
        system : micromagneticmodel.System

            System object to be driven.

        dirname : str, optional

            Name of a base directory in which the simulation results are stored.
            Additional subdirectories based on the system name and the current drive
            number are created automatically (``dirname/<system-name>/drive-<number>``).
            If not specified the current workinng directory is used.

        append : bool, optional

            If ``True`` and the system directory already exists, drive or compute
            directories will be appended. Defaults to ``True``.

        runner : micromagneticmodel.ExternalRunner, optional

            External Runner which is going to be used for running the calculation. If
            ``None``, a runner will be found automatically. Defaults to ``None``.

        ovf_format : str

            Format of the magnetisation output files written by the external simulation
            tool. Can be one of ``'bin8'`` (binary, double precision), ``'bin4'``
            (binary, single precision) or ``'txt'`` (text-based, double precision).
            Defaults to ``'bin8'``.

        verbose : int, optional

            If ``verbose=0``, no output is printed. For ``verbose=1`` information about
            the runner and the runtime is printed to stdout. For ``verbose=2`` a
            progress bar is displayed for time drives. Note that this information
            only relies on the number of magnetisation snapshots already saved to disk
            and therefore only gives a rough indication of progress. Defaults to ``1``.

        Raises
        ------
        FileExistsError

            If system directory already exists and append=False.

        """
        # This method is implemented in the derived driver class. It raises
        # exception if any of the arguments are not valid.
        self.drive_kwargs_setup(**kwargs)

        workingdir = self._setup_working_directory(
            system=system, dirname=dirname, mode="drive", append=append
        )

        with uu.changedir(workingdir):
            self._write_input_files(
                system=system,
                ovf_format=ovf_format,
                **kwargs,
            )
            self._call(system=system, runner=runner, verbose=verbose, **kwargs)
            self._read_data(system)

        system.drive_number += 1

    def schedule(
        self,
        system,
        cmd,
        header,
        script_name="job.sh",
        dirname=".",
        append=True,
        runner=None,
        ovf_format="bin8",
        verbose=1,
        **kwargs,
    ):
        """Schedule drive of the system in phase space.

        Takes ``micromagneticmodel.System`` and drives it in phase space. This method
        writes the input files for the external package and then submits a job to the
        machine's job scheduling system, e.g. Slurm. The command to schedule and the
        required resources in a format understood by the schedule command must be passed
        to the function.

        It is the user's responsibility to ensure that the external package can be
        executed from the scheduled job.

        If ``append=True`` and the system director already exists, drive will
        be appended to that directory. Otherwise, an exception will be raised.

        This method accepts any other arguments that could be required by the
        specific driver.

        Parameters
        ----------
        system : micromagneticmodel.System

            System object to be driven.

        cmd : str

            Name of the scheduling system's submission program, e.g. ``'sbatch'`` for
            Slurm.

        header : str

            Filename of the submission header file or str with the data to specify
            system requirements such as number of CPUs and memory.

        script_name : str, optional

            Name of the newly created OOMMF run script that is scheduled for execution.

        dirname : str, optional

            Name of a base directory in which the simulation results are stored.
            Additional subdirectories based on the system name and the current drive
            number are created automatically. If not specified the current working
            directory is used.

        append : bool, optional

            If ``True`` and the system directory already exists, drive or
            compute directories will be appended. Defaults to ``True``.

        runner : micromagneticmodel.ExternalRunner, optional

            External Runner which is going to be used for running the calculation. If
            ``None``, a runner will be found automatically. Defaults to ``None``.

        ovf_format : str

            Format of the magnetisation output files written by The external package.
            Can be one of ``'bin8'`` (binary, double precision), ``'bin4'`` (binary,
            single precision) or ``'txt'`` (text-based, double precision). Defaults to
            ``'bin8'``.

        verbose : int, optional

            If ``verbose=0``, no output is printed. For ``verbose=1`` information about
            the submitted job is printed to stdout.

        Raises
        ------
        FileExistsError

            If system directory already exists and append=False.

        """
        # This method is implemented in the derived driver class. It raises
        # exception if any of the arguments are not valid.
        self.schedule_kwargs_setup(**kwargs)

        workingdir = self._setup_working_directory(
            system=system, dirname=dirname, mode="drive", append=append
        )

        # Convert to absolute path if it is a file name because the file will be
        # accessed from a different directory.
        if pathlib.Path(header).exists():
            header = pathlib.Path(header).absolute()

        with uu.changedir(workingdir):
            self._write_input_files(
                system=system,
                ovf_format=ovf_format,
                **kwargs,
            )
            self._write_schedule_script(
                system=system, header=header, script_name=script_name, runner=runner
            )

            stdout = stderr = sp.PIPE
            if sys.platform == "win32":
                stdout = stderr = None  # pragma: no cover

            if verbose >= 1:
                print(f"Running '{cmd} {script_name}' in '{workingdir.absolute()}'.")
            system.drive_number += 1
            res = sp.run([cmd, script_name], stdout=stdout, stderr=stderr)

            if res.returncode != 0:
                msg = "Error during job schedule.\n"
                msg += f"command: {cmd} {script_name}\n"
                if sys.platform != "win32":
                    # Only on Linux and MacOS - on Windows we do not get stderr and
                    # stdout.
                    stderr = res.stderr.decode("utf-8", "replace")
                    stdout = res.stdout.decode("utf-8", "replace")
                    msg += f"stdout: {stdout}\n"
                    msg += f"stderr: {stderr}\n"
                raise RuntimeError(msg)

    def _write_schedule_script(self, system, header, script_name, runner):
        if pathlib.Path(header).exists():
            with open(header, "rt", encoding="utf-8") as f:
                header = f.read()
        else:
            header = header
        run_cmd = self._call(system=system, runner=runner, dry_run=True)
        with open(script_name, "wt", encoding="utf-8") as f:
            f.write(header)
            f.write("\n")
            f.write(" ".join(run_cmd))

    def _write_info_json(self, system, **kwargs):
        info = {}
        info["drive_number"] = system.drive_number
        info["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        info["time"] = datetime.datetime.now().strftime("%H:%M:%S")
        info["driver"] = self.__class__.__name__
        for k, v in kwargs.items():
            info[k] = v
        with open("info.json", "wt", encoding="utf-8") as jsonfile:
            jsonfile.write(json.dumps(info))

    @staticmethod
    def _setup_working_directory(system, dirname, mode, append=True):
        system_dir = pathlib.Path(dirname, system.name)
        if system_dir.exists() and not append:
            raise FileExistsError(
                f"Directory {system.name=} already exists. To "
                "append drives to it, pass append=True."
            )
        try:
            last_existing_simulation = max(
                system_dir.glob(f"{mode}*"), key=lambda p: int(p.name.split("-")[1])
            )
            next_number = int(last_existing_simulation.name.split("-")[1]) + 1
        except ValueError:  # glob did not find any directories
            next_number = 0
        setattr(system, f"{mode}_number", next_number)
        workingdir = system_dir / f"{mode}-{next_number}"
        workingdir.mkdir(parents=True)
        return workingdir

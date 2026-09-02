import abc
import datetime
import importlib.metadata
import json
import math
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
    """Base class for existing external simulation packages (e.g. OOMMF, mumax3).

    A `Driver` corresponds to a type of simulation, e.g. energy minimisation or LLG time
    evolution. The `Driver` takes a ``system`` object and translates it into
    calculator-specific input files that it stores in a new `drive` directory. It then
    calls a `Runner`, which will trigger the actual simulation. Once the simulation is
    complete, the `Driver` reads the final state and updates the ``system`` object.

    This class provides a scaffold for performing such simulations. Adapter packages
    inherit from this base class and need to implement a number of abstract methods to
    control calculator-specific behaviour and functionality.

    This class is suitable for adapters that communicate with their calculator by first
    writing input files to disk and then executing the calculator in a subprocess.
    """

    @property
    @abc.abstractmethod
    def _x(self):
        """Independent variable.

        The independent variable of a simulation depends on its type. Common examples
        are `t` for time integration and `iteration` for energy minimisation. It should
        match the column name used in the tabular output produced by the calculator and
        can be used to update `system.table` in the `ExternalDriver._read_data` method.
        """

    @abc.abstractmethod
    def drive_kwargs_setup(self, drive_kwargs):
        """Check and initialise kwargs for drive.

        The user can pass arbitrary keyword arguments to ``drive``. This method needs
        to validate and document the list of allowed keyword arguments. Any
        modifications or setting defaults need to be done in-place.
        """

    @abc.abstractmethod
    def schedule_kwargs_setup(self, schedule_kwargs):
        """Check and initialise kwargs for schedule.

        The user can pass arbitrary keyword arguments to ``schedule``. This method needs
        to validate and document the list of allowed keyword arguments. Any
        modifications or setting defaults need to be done in-place.
        """

    @abc.abstractmethod
    def _write_input_files(self, system, **kwargs):
        """Write input files required for the external package."""

    @abc.abstractmethod
    def _call(self, system, runner, **kwargs):
        """Call the external package.

        This method is called to run the actual simulation. It is executed in the
        directory where the input files have been written. The implementation should
        communicate with a `Runner` and trigger the simulation using `Runner.call`. If
        `runner=None` it should pick a suitable runner.

        This method should pass suitable flags/options to the `argstr` argument of
        `Runner.call` that are needed to trigger the simulation of this specific type of
        drive. The `Runner` class takes care about finding the right executable and
        passing these arguments to it.
        """

    @abc.abstractmethod
    def _schedule_commands(self, system, runner):
        """Return a list of commands to append to the scheduling script.

        This method should make use of the dry-run capabilities of the `Runner.call`
        method to obtain a command that can run the simulation. This command will be
        appended to the scheduling script and will be executed in the directory where
        the input files have been written. If `runner=None` it should pick a suitable
        runner.
        """

    @abc.abstractmethod
    def _read_data(self, system):
        """Update system with simulation output (magnetisation and scalar data).

        This method is called after the simulation has finished. It should read the
        (final) simulation output and update the system object by:
        - setting `system.m` to the final state
        - reading scalar data of the current drive and setting `system.table`

        This method is called in the directory where the input files have been written.
        """

    @abc.abstractmethod
    def _check_system(self, system):
        """Check if the system contains all required information.

        This method is called before creating input files. It can be used to perform
        drive/calculator-specific checks, e.g. to ensure that the energy or dynamics
        equations are non-empty.
        """

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

        kwargs

            Additional calculator-specific keyword arguments can be passed. These are
            documented in ``drive_kwargs_setup`` of the individual calculators.

        Raises
        ------
        FileExistsError

            If system directory already exists and append=False.

        """
        drive_kwargs = kwargs.copy()
        # This method is implemented in the derived driver class. It raises
        # exception if any of the arguments are not valid.
        self.drive_kwargs_setup(kwargs)
        self._check_system(system)
        workingdir = self._setup_working_directory(
            system=system, dirname=dirname, mode="drive", append=append
        )
        start_time = datetime.datetime.now()

        with uu.changedir(workingdir):
            self._write_input_files(
                system=system,
                ovf_format=ovf_format,
                **kwargs,
            )

            self._write_info_json(system, start_time, **drive_kwargs)
            try:
                self._call(system=system, runner=runner, verbose=verbose, **kwargs)
            except Exception:
                success = False
                raise
            else:
                success = True
            finally:
                end_time = datetime.datetime.now()
                self._update_info_json(start_time, end_time, success)
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

        kwargs

            Additional calculator-specific keyword arguments can be passed. These are
            documented in ``schedule_kwargs_setup`` of the individual calculators.

        Raises
        ------
        FileExistsError

            If system directory already exists and append=False.

        """
        schedule_kwargs = kwargs.copy()
        # This method is implemented in the derived driver class. It raises
        # exception if any of the arguments are not valid.
        self.schedule_kwargs_setup(kwargs)
        self._check_system(system)
        workingdir = self._setup_working_directory(
            system=system, dirname=dirname, mode="drive", append=append
        )

        # Convert to absolute path if it is a file name because the file will be
        # accessed from a different directory.
        if pathlib.Path(header).exists():
            header = pathlib.Path(header).absolute()

        start_time = datetime.datetime.now()

        with uu.changedir(workingdir):
            self._write_input_files(
                system=system,
                ovf_format=ovf_format,
                **kwargs,
            )
            self._write_schedule_script(
                system=system, header=header, script_name=script_name, runner=runner
            )
            self._write_info_json(system, start_time, **schedule_kwargs)

            stdout = stderr = sp.PIPE
            if sys.platform == "win32":
                stdout = stderr = None  # pragma: no cover

            if verbose >= 1:
                print(
                    f"Running '{cmd} {script_name}' in '{pathlib.Path().absolute()}'."
                )
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
        """
        Scheduling systems such as slurm typically need a script that will be run. This
        method creates the script `script_name` by combining:

        - a user provided `header` (either a file on disk that will be read or a str);
          the header needs to contain all scheduler-specific code such as required
          resources, runtime, name, ... (for slurm this would be ``#SBATCH ...`` lines).

          The user needs to also ensure that the environment launched by the scheduling
          system provides the external calculator executable, e.g. by modifying PATH
          or loading a suitable (conda) environment.
        - a call to the external calculator that triggers the simulation, provided by
          the method `_schedule_command`
        """
        if pathlib.Path(header).exists():
            with open(header, encoding="utf-8") as f:
                header = f.read()
        else:
            header = header
        run_commands = self._schedule_commands(system=system, runner=runner)
        with open(script_name, "w", encoding="utf-8") as f:
            f.write(header)
            f.write("\n")
            f.write("\n".join(run_commands))

    def _write_info_json(self, system, start_time, **kwargs):
        """
        Each drive contains a file ``info.json`` that contains metadata about the
        simulation such as date/time/index/used adapater, and can additionally contain
        arbitrary user-provided key-value pairs, provided these can be serialised to
        json.
        """
        info = {}
        info["drive_number"] = system.drive_number
        info["date"] = start_time.strftime("%Y-%m-%d")
        info["time"] = start_time.strftime("%H:%M:%S")
        info["start_time"] = start_time.isoformat(timespec="seconds")
        # "adapter" is the ubermag package (e.g. oommfc) that communicates with the
        # calculator (e.g. OOMMF)
        info["adapter"] = self.__module__.split(".")[0]
        info["adapter_version"] = importlib.metadata.version(
            self.__module__.split(".")[0]
        )
        info["driver"] = self.__class__.__name__
        for key, value in kwargs.items():
            info.setdefault(key, value)

        with open("info.json", "w", encoding="utf-8") as jsonfile:
            jsonfile.write(json.dumps(info))

    @staticmethod
    def _setup_working_directory(system, dirname, mode, append=True):
        """
        This function creates a new directory of the form
        `dirname/system.name/mode-<index>`. For `append=True` the <index> is determined
        automatically by searching for all existing `mode-<index>` directories. For
        `append=False` the base directory `dirname/system.name` must not exist.
        """
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

    @staticmethod
    def _conversion_to_hms(time_difference):
        total_seconds = math.ceil(time_difference.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def _update_info_json(self, start_time, end_time, success):
        with open("info.json", encoding="utf-8") as jsonfile:
            info = json.load(jsonfile)
        info["end_time"] = end_time.isoformat(timespec="seconds")
        info["elapsed_time"] = self._conversion_to_hms(end_time - start_time)
        info["success"] = success
        with open("info.json", "w", encoding="utf-8") as jsonfile:
            json.dump(info, jsonfile)

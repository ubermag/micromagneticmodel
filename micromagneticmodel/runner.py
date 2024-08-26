import abc
import sys

import ubermagutil as uu


class ExternalRunner(abc.ABC):
    @property
    @abc.abstractmethod
    def package_name(self):
        """Name of the external simulation package."""

    @abc.abstractmethod
    def _call(self, argstr, need_stderr, dry_run, **kwargs):
        """Package-specific implementation to run the simulation."""

    def call(
        self,
        argstr,
        need_stderr=False,
        verbose=1,
        total=None,
        glob_name="",
        **kwargs,
    ):
        """Call an external simulation package by passing ``argstr`` to it.

        Parameters
        ----------
        argstr : str

            Argument string passed to the external package.

        need_stderr : bool, optional

            If ``need_stderr=True``, standard error is captured. Defaults to ``False``.

        verbose : int, optional

            If ``verbose=0``, no output is printed. For ``verbose=1`` information about
            the runner and the runtime is printed to stdout. For ``verbose=2`` a
            progress bar is displayed for time drives. Note that this information
            only relies on the number of magnetisation snapshots already saved to disk
            and therefore only gives a rough indication of progress. Defaults to ``1``.

        total : int, optional

            Number of magnetisation snapshots that the external package writes during
            the simulation. This information is used to update the progress bar.

        glob_name : str, optional

            Glob expression to find the magnetisation snapshots that the external
            package writes during the simulation. This information is used to update the
            progress bar.

        Raises
        ------
        RuntimeError

            If an error occured.

        Returns
        -------
        int

            Return code of the runner, 0 if the run was successful.

        """
        if verbose >= 2 and total:
            context = uu.progress.bar(
                total=total,
                package_name=self.package_name,
                runner_name=self.__class__.__name__,
                glob_name=glob_name,
            )
        elif verbose >= 1:
            context = uu.progress.summary(
                package_name=self.package_name, runner_name=self.__class__.__name__
            )
        else:
            context = uu.progress.quiet()

        with context:
            res = self._call(argstr=argstr, need_stderr=need_stderr, **kwargs)

        if res.returncode != 0:
            msg = f"Error in {self.package_name} run.\n"
            msg += f"command: {' '.join(res.args)}\n"
            if sys.platform != "win32":
                # Only on Linux and MacOS - on Windows we do not get stderr and
                # stdout.
                msg += f"stdout: {res.stderr.decode('utf-8', 'replace')}\n"
                msg += f"stderr: {res.stdout.decode('utf-8', 'replace')}\n"
            raise RuntimeError(msg)

        return res

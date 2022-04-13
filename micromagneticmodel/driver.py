import abc

import micromagneticmodel as mm


class Driver(mm.abstract.Abstract):
    """An abstract class for deriving drivers."""

    @abc.abstractmethod
    def drive(self, system, **kwargs):
        """Drive method.

        This method must be implemented by a specific micromagnetic calculator.

        """
        pass  # pragma: no cover

import abc


class ExternalRunner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def call(self, dry_run=False, **kwargs):
        """Call the external simulation package."""

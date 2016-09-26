import micromagneticmodel.util.typesystem as ts
from micromagneticmodel import System


@ts.typesystem(system=ts.TypedAttribute(expected_type=System),
               t=ts.UnsignedReal,
               n=ts.UnsignedInt,
               name=ts.String)
class Driver(object):
    def __init__(self, system, **kwargs):
        self.system = system
        for key, value in kwargs.items():
            setattr(self, key, value)

    def drive(self):
        raise NotImplementedError

    def script(self):
        raise NotImplementedError

    def run_simulator(self):
        raise NotImplementedError

    def update_system(self):
        raise NotImplementedError

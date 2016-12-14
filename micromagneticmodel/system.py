import importlib
import discretisedfield as df
import micromagneticmodel as mm
import joommfutil.typesystem as ts


@ts.typesystem(name=ts.ObjectName)
class System:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in ["hamiltonian", "dynamics", "m", "name"]:
                setattr(self, key, value)
            else:
                raise AttributeError("Unexpected kwarg {}.".format(key))

        self.module = importlib.__import__(self.__class__.__module__)
        if "hamiltonian" not in self.__dict__:
            self.hamiltonian = 0
        if "dynamics" not in self.__dict__:
            self.dynamics = 0

    @property
    def hamiltonian(self):
        return self._hamiltonian

    @hamiltonian.setter
    def hamiltonian(self, value):
        self._hamiltonian = self.module.Hamiltonian()
        setattr(self._hamiltonian, "_system", self)
        if value == 0:
            pass
        elif isinstance(value, (mm.EnergyTerm, mm.Hamiltonian)):
            self._hamiltonian += value
        else:
            raise TypeError("Unsupported type(value)={}".format(type(value)))

    @property
    def dynamics(self):
        return self._dynamics

    @dynamics.setter
    def dynamics(self, value):
        self._dynamics = self.module.Dynamics()
        setattr(self._dynamics, "_system", self)
        if value == 0:
            pass
        elif isinstance(value, (mm.DynamicsTerm, mm.Dynamics)):
            self._dynamics += value
        else:
            raise TypeError("Unsupported type(value)={}".format(type(value)))

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        if isinstance(value, df.Field):
            self._m = value
        else:
            raise TypeError("Unsupported type(m)={}".format(type(value)))

    @property
    def script(self):
        raise NotImplementedError

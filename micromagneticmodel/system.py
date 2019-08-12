import importlib
import discretisedfield as df
import micromagneticmodel as mm
import ubermagutil.typesystem as ts


@ts.typesystem(name=ts.Name(const=True))
class System:
    _attributes = ["hamiltonian", "dynamics", "m", "name"]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in System._attributes:
                setattr(self, key, value)
            else:
                raise AttributeError("Unexpected kwarg {}.".format(key))

        self._module = importlib.__import__(self.__class__.__module__)
        if "hamiltonian" not in self.__dict__:
            self.hamiltonian = 0
        if "dynamics" not in self.__dict__:
            self.dynamics = 0

        self.drive_number = 0

    @property
    def hamiltonian(self):
        return self._hamiltonian

    @hamiltonian.setter
    def hamiltonian(self, value):
        self._hamiltonian = self._module.Hamiltonian()
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
        self._dynamics = self._module.Dynamics()
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
    def _script(self):
        raise NotImplementedError

    def __repr__(self):
        r = ["System object '{}':".format(self.name)]
        for attribute in System._attributes:
            if attribute == 'name':
                continue
            r.append("\t{:11}: {}".format(attribute,
                                          getattr(self, attribute, "")))
        return "\n".join(r)

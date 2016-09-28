import importlib
import micromagneticmodel.util.typesystem as ts
from discretisedfield import Field
from .hamiltonian import Hamiltonian
from .dynamics import Dynamics
from discretisedfield import Mesh, Field


@ts.typesystem(name=ts.String,
               mesh=ts.TypedAttribute(expected_type=Mesh),
               hamiltonian=ts.TypedAttribute(expected_type=Hamiltonian),
               dynamics=ts.TypedAttribute(expected_type=Dynamics))
class System:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in ["mesh", "hamiltonian", "dynamics", "m", "name"]:
                setattr(self, key, value)
            else:
                raise AttributeError("Unexpected kwarg {}.".format(key))

        selfmodule = importlib.__import__(self.__class__.__module__)
        if "hamiltonian" not in self.__dict__:
            self.hamiltonian = selfmodule.Hamiltonian()
        if "dynamics" not in self.__dict__:
            self.dynamics = selfmodule.Dynamics()

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        if isinstance(value, Field):
            self._m = value
        else:
            m_field = Field(self.mesh, dim=3, value=value)
            self._m = m_field

    def script(self):
        raise NotImplementedError

    def total_energy(self):
        raise NotImplementedError

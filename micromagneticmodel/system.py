import importlib
from discretisedfield import Field
from .hamiltonian import Hamiltonian, EnergyTerm
from .dynamics import Dynamics, DynamicsTerm
from discretisedfield import Mesh, Field
import micromagneticmodel.util.typesystem as ts


@ts.typesystem(name=ts.String,
               mesh=ts.TypedAttribute(expected_type=Mesh))
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
    def hamiltonian(self):
        return self._hamiltonian

    @hamiltonian.setter
    def hamiltonian(self, value):
        if isinstance(value, Hamiltonian):
            self._hamiltonian = value
        elif isinstance(value, EnergyTerm):
            hamiltonian = Hamiltonian()
            hamiltonian += value
            self._hamiltonian = hamiltonian
        else:
            raise TypeError("Expected EnergyTerm or Hamiltonian.")

    @property
    def dynamics(self):
        return self._dynamics

    @dynamics.setter
    def dynamics(self, value):
        if isinstance(value, Dynamics):
            self._dynamics = value
        elif isinstance(value, DynamicsTerm):
            dynamics = Dynamics()
            dynamics += value
            self._dynamics = dynamics
        else:
            raise TypeError("Expected DynamicsTerm or Dynamics.")

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

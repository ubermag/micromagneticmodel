import micromagneticmodel.util.typesystem as ts
from numbers import Real
from discretisedfield import Field
from .hamiltonian import Hamiltonian
from .dynamics import Dynamics
from discretisedfield import Mesh, Field


@ts.typesystem(Ms=ts.PositiveReal,
               name=ts.String)
class System:
    def __init__(self, mesh, Ms, name=None):
        if not isinstance(mesh, Mesh):
            raise TypeError('mesh must be of type Mesh.')

        self.mesh = mesh
        self.Ms = Ms
        self.name = name

        self.hamiltonian = Hamiltonian()
        self.dynamics = Dynamics()

        self.m = Field(self.mesh, dim=3)

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        m_field = Field(self.mesh, dim=3)
        m_field.set(value)
        self._m = m_field

    def total_energy(self):
        raise NotImplementedError

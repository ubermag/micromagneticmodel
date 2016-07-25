import abc
import six
from numbers import Real
from finitedifferencefield import Field
from micromagneticmodel.hamiltonian import Hamiltonian
from micromagneticmodel.dynamics import Dynamics
from micromagneticmodel.mesh import MeshAbstract
from energies import Zeeman


@six.add_metaclass(abc.ABCMeta)
class SimAbstract(object):
    def __init__(self, mesh, Ms, name=None):
        if not isinstance(mesh, MeshAbstract):
            raise ValueError('mesh must be of type MeshAbstract.')
        if not isinstance(Ms, Real) or Ms <= 0:
            raise ValueError('Ms must be a positive real number.')
        if not isinstance(name, str):
            raise ValueError('name must be a string.')
        self.mesh = mesh
        self.Ms = Ms
        self.name = name

        self.hamiltonian = Hamiltonian()
        self.dynamics = Dynamics()

        self.dirname = self.name + '/'
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

        self.m =  Field(self.atlas.cmin, self.atlas.cmax, self.mesh.d, dim=3)

        self.t = 0
        
    def set_m(self, m0):
        self.m0 = m0

    def set_H(self, H):
        print("MicromagneticModel: setting field = {}")
        for energy in self.energies:
            if isinstance(energy, Zeeman):
                self.energies.remove(energy)
        self.add(Zeeman(H))

    @abc.abstractmethod
    def relax(self): pass

    @abc.abstractmethod
    def m_average(self): pass

    @abc.abstractmethod
    def total_energy(self): pass

    

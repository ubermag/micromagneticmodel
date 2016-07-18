from energies import Hamiltonian
from dynamics import Dynamics
from energies import Zeeman
from finitedifferencefield import Field


class MicromagneticModel(object):
    def __init__(self, mesh, Ms, name=None):
        self.mesh = mesh
        self.Ms = Ms
        self.name = name

        self.hamiltonian = Hamiltonian()
        self.dynamics = Dynamics()

        #self.m = Field()
        self.t = 0

    def __str__(self):
        return "MicromagneticModel(name={})".format(self.name)

    def add_energy(self, energy):
        self.hamiltonian.add(energy)

    def add_dynamics(self, dynamics):
        self.dynamics.add(dynamics)

    def show_hamiltonian(self):
        return self.hamiltonian.show()

    def show_dynamics(self):
        return self.dynamics.show()

    def show_mesh(self):
        self.mesh.show()

    def set_m(self, m0):
        self.m0 = m0

    def set_H(self, H):
        print("MicromagneticModel: setting field = {}")
        for energy in self.energies:
            if isinstance(energy, Zeeman):
                self.energies.remove(energy)
        self.add(Zeeman(H))

    def relax(self):
        raise NotImplementedError("relax is abstract method")

    def m_average(self):
        raise NotImplementedError("m_average is abstract method")

    def total_energy(self):
        raise NotImplementedError("total_energy is abstract method")
    
    def hysteresis(self, fieldlist):
        print("AbstractMicromagneticModell: starting hysteresis")
        for field in fieldlist:
            self.set_H(field)
            self._relax()

import pytest
import micromagneticmodel as mm


class TestEnergyProperties:
    def setup(self):
        self.system = mm.System()
        self.system.hamiltonian = mm.Exchange(A=1)

    def test_data(self):
        assert isinstance(self.system.hamiltonian.exchange._data, mm.Data)
        assert isinstance(self.system.hamiltonian._data, mm.Data)

    def test_energy(self):
        with pytest.raises(NotImplementedError):
            energy = self.system.hamiltonian.energy
        with pytest.raises(NotImplementedError):
            energy = self.system.hamiltonian.exchange.energy

    def test_energy_density(self):
        with pytest.raises(NotImplementedError):
            energy = self.system.hamiltonian.energy_density
        with pytest.raises(NotImplementedError):
            energy = self.system.hamiltonian.exchange.energy_density

    def test_effective_field(self):
        with pytest.raises(NotImplementedError):
            energy = self.system.hamiltonian.effective_field
        with pytest.raises(NotImplementedError):
            energy = self.system.hamiltonian.exchange.effective_field

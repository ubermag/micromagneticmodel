import pytest
import micromagneticmodel as mm


class TestEnergyProperties:
    def setup(self):
        self.ep = mm.EnergyProperties()

    def test_energy(self):
        with pytest.raises(NotImplementedError):
            energy = self.ep.energy

    def test_energy_density(self):
        with pytest.raises(NotImplementedError):
            energy_density = self.ep.energy_density

    def test_effective_field(self):
        with pytest.raises(NotImplementedError):
            effective_field = self.ep.effective_field

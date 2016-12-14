import pytest
import micromagneticmodel as mm


class TestData:
    def setup(self):
        self.data = mm.Data(system=None, cls=None)

    def test_energy(self):
        with pytest.raises(NotImplementedError):
            energy = self.data.energy

    def test_energy_density(self):
        with pytest.raises(NotImplementedError):
            energy = self.data.energy_density

    def test_effective_field(self):
        with pytest.raises(NotImplementedError):
            energy = self.data.effective_field

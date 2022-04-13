import discretisedfield as df
import pytest

import micromagneticmodel as mm

from .checks import check_system


class TestSystem:
    def setup(self):
        p1 = (0, 0, 0)
        p2 = (10e-9, 10e-9, 10e-9)
        n = (10, 10, 10)
        Ms = 1e6
        region = df.Region(p1=p1, p2=p2)
        mesh = df.Mesh(region=region, n=n)
        self.m = df.Field(mesh=mesh, dim=3, value=(0, 1, 1), norm=Ms)

    def test_init_valid_args(self):
        system = mm.System()
        check_system(system)
        assert len(system.energy) == 0
        assert len(system.dynamics) == 0
        assert system.m is None
        assert system.T == 0
        assert system.name == "unnamed"  # Default value

        system.energy = mm.Exchange(A=1e-12) + mm.Demag()
        check_system(system)
        assert len(system.energy) == 2

        system.dynamics = mm.Precession(gamma0=2.21e5) + mm.Damping(alpha=1)
        check_system(system)
        assert len(system.dynamics) == 2

        system.m = self.m
        system.T = 5
        check_system(system)

    def test_init_invalid_args(self):
        with pytest.raises(TypeError):
            mm.System(energy=5)

        with pytest.raises(TypeError):
            mm.System(dynamics=5)

        with pytest.raises(TypeError):
            mm.System(name=152)

        with pytest.raises(ValueError):
            mm.System(T=-0.1)

        with pytest.raises(TypeError):
            mm.System(m=-0.1)

    def test_repr(self):
        system = mm.System(name="my_very_cool_system")
        check_system(system)
        assert repr(system) == "System(name='my_very_cool_system')"

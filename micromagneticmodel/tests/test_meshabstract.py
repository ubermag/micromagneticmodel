import pytest
from micromagneticmodel.mesh import MeshAbstract


class Mesh(MeshAbstract):
    """Implementation of the abstract class for testing."""
    def calculator_script(self):
        raise NotImplementedError()


class TestMeshAbstract(object):
    def setup(self):
        self.valid_args = [[(0, 0, 0),
                            (5, 5, 5),
                            (1, 1, 1)],
                           [(0, 0, 0),
                            [5e-9, 5e-9, 5e-9],
                            (1e-9, 1e-9, 1e-9)],
                           [(-1.5e-9, -5e-9, 0),
                            (1.5e-9, 15e-9, 16e-9),
                            (5, 1, 1e-9)],
                           [(-1.5e-9, -5e-9, -5e-9),
                            (0, 0, 0),
                            (1.0, 13-6, 1.1e4)]]

        self.invalid_args = [[(0, 0, 0),
                              (5, 5, 5),
                              (-1, 1, 1)],
                             ['1',
                              (1, 1, 1),
                              (0, 0, 1e-9)],
                             [(-1.5e-9, -5e-9, 0),
                              (1.5e-9, 15e-9, 16e-9),
                              (5, 1, -1e-9)],
                             [(-1.5e-9, -5e-9, 0),
                              (1.5e-9, 15e-9, 16e-9),
                              (-2e-9, 1, 1e-9)],
                             ['string', (5, 1, 1e-9), 'string'],
                             [(-1.5e-9, -5e-9, 0),
                              (1.5e-9, 15e-9, 16e-9),
                              1]]

    def test_abstract_class(self):
        for arg in self.valid_args:
            with pytest.raises(TypeError):
                cmin = arg[0]
                cmax = arg[1]
                d = arg[2]

                meshabstract = MeshAbstract(cmin, cmax, d)

    def test_init_valid_args(self):
        for arg in self.valid_args:
            cmin = arg[0]
            cmax = arg[1]
            d = arg[2]

            mesh = Mesh(cmin, cmax, d)

            assert mesh.cmin == cmin
            assert mesh.cmax == cmax
            assert mesh.d == d

    def test_init_invalid_args(self):
        for arg in self.invalid_args:
            with pytest.raises(ValueError):
                cmin = arg[0]
                cmax = arg[1]
                d = arg[2]

                mesh = Mesh(cmin, cmax, d)

    def test_name(self):
        for arg in self.valid_args:
            cmin = arg[0]
            cmax = arg[1]
            d = arg[2]

            mesh = Mesh(cmin, cmax, d)

            assert mesh._name == 'mesh'

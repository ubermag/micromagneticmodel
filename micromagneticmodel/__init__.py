import pytest
import pkg_resources
import micromagneticmodel.consts
import micromagneticmodel.util  # to avoid import order conflicts
from .energy import Exchange, Zeeman, UniaxialAnisotropy, \
    CubicAnisotropy, Demag, Zeeman, DMI, Energy
from .dynamics import Precession, Damping, ZhangLi, Dynamics
from .evolvers import Evolver
from .drivers import Driver
from .system import System


def test():
    return pytest.main(["-v", "--pyargs",
                        "micromagneticmodel"])  # pragma: no cover


__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)

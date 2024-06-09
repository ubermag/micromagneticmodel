"""Domain-specific language for computational magnetism."""

import importlib.metadata

import pytest

from . import abstract as abstract
from . import consts as consts
from . import examples as examples
from .driver import Driver as Driver
from .driver import ExternalDriver as ExternalDriver
from .dynamics import Damping as Damping
from .dynamics import Dynamics as Dynamics
from .dynamics import DynamicsTerm as DynamicsTerm
from .dynamics import Precession as Precession
from .dynamics import Slonczewski as Slonczewski
from .dynamics import ZhangLi as ZhangLi
from .energy import DMI as DMI
from .energy import RKKY as RKKY
from .energy import CubicAnisotropy as CubicAnisotropy
from .energy import Demag as Demag
from .energy import Energy as Energy
from .energy import EnergyTerm as EnergyTerm
from .energy import Exchange as Exchange
from .energy import MagnetoElastic as MagnetoElastic
from .energy import UniaxialAnisotropy as UniaxialAnisotropy
from .energy import Zeeman as Zeeman
from .evolver import Evolver as Evolver
from .runner import ExternalRunner as ExternalRunner
from .system import System as System

__version__ = importlib.metadata.version(__package__)


def test():
    """Run all package tests.

    Examples
    --------
    1. Run all tests.

    >>> import micromagneticmodel
    ...
    >>> # micromagneticmodel.test()

    """
    return pytest.main(
        ["-v", "--pyargs", "micromagneticmodel", "-l"]
    )  # pragma: no cover

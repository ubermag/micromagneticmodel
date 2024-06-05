"""Domain-specific language for computational magnetism."""

import importlib.metadata

import pytest

import micromagneticmodel.abstract as abstract
import micromagneticmodel.consts as const
import micromagneticmodel.examples as examples
from .driver import Driver as Driver
from .driver import ExternalDriver as ExternalDriver
from .dynamics import Damping as Damping
from .dynamics import Dynamics as Dynamics
from .dynamics import DynamicsTerm as DynamicsTerm
from .dynamics import Precession as Precession
from .dynamics import Slonczewski as Slonczewski
from .dynamics import ZhangLi as ZhangLi
from .energy import (
    DMI as DMI,
    RKKY as RKKY,
    CubicAnisotropy as CubicAnisotropy,
    Demag as Demag,
    Energy as Energy,
    EnergyTerm as EnergyTerm,
    Exchange as Exchange,
    MagnetoElastic as MagnetoElastic,
    UniaxialAnisotropy as UniaxialAnisotropy,
    Zeeman as Zeeman,
)
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

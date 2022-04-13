import numbers
import re
import types

import discretisedfield as df
import pytest

import micromagneticmodel as mm


def check_term(term):
    assert isinstance(term, mm.abstract.Term)

    assert isinstance(term._allowed_attributes, list)
    assert len(term._allowed_attributes) > 0

    if isinstance(term, mm.energy.energyterm.EnergyTerm):
        assert isinstance(getattr(mm, term._container_class)(), mm.Energy)
        with pytest.raises(NotImplementedError):
            term.effective_field(m=None)
        with pytest.raises(NotImplementedError):
            term.energy(m=None)
        with pytest.raises(NotImplementedError):
            term.density(m=None)
    else:
        assert isinstance(getattr(mm, term._container_class)(), mm.Dynamics)
        with pytest.raises(NotImplementedError):
            term.dmdt(m=None, Heff=None)

    assert term == term
    assert not term != term
    assert term != "5"

    container = getattr(mm, term._container_class)()
    check_container(container)
    assert len(container) == 0
    container += term
    check_container(container)
    assert len(container) == 1
    assert term in container

    assert getattr(container, term.name) == term
    assert term.name in dir(container)

    container -= term
    check_container(container)
    assert len(container) == 0
    assert term not in container

    # Try to add two terms of the same type.
    with pytest.raises(ValueError):
        container = term + term

    assert isinstance(repr(term), str)
    assert re.search(r"^.+\(.*\)$", repr(term))

    assert isinstance(term._repr_latex_(), str)
    assert re.search(r"^\$.+\$$", term._repr_latex_())

    assert isinstance(term.name, str)
    assert re.search(r"\w+", term.name)


def check_container(container):
    assert isinstance(container, mm.abstract.Container)
    assert isinstance(container._terms, list)

    if isinstance(container, mm.Energy):
        assert container._term_class.__name__ == "EnergyTerm"
    else:
        assert container._term_class.__name__ == "DynamicsTerm"

    assert isinstance(len(container), int)
    assert len(container) >= 0

    assert isinstance(iter(container), types.GeneratorType)
    assert list(container) == container._terms
    assert len(list(container)) == len(container)

    for term in container:
        assert term in container
        assert isinstance(getattr(container, term.name), mm.abstract.Term)
        assert getattr(container, term.name) == term
        assert term.name in dir(container)

    assert container == container
    assert not container != container
    assert container != "5"

    # neutral element for addition
    assert container + container.__class__() == container

    assert isinstance(dir(container), list)

    assert isinstance(repr(container), str)

    assert isinstance(container._repr_latex_(), str)
    assert re.search(r"^\$.+\$$", container._repr_latex_())


def check_system(system):
    assert isinstance(system, mm.System)

    assert isinstance(system.energy, mm.Energy)
    check_container(system.energy)

    assert isinstance(system.dynamics, mm.Dynamics)
    check_container(system.dynamics)

    assert isinstance(system.T, numbers.Real)
    assert system.T >= 0

    assert isinstance(system.name, str)

    if system.m is not None:
        assert isinstance(system.m, df.Field)

    assert isinstance(repr(system), str)
    assert re.search(r"^System\(name=.+\)$", repr(system))

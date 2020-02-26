import re
import types
import pytest
import micromagneticmodel as mm


def check_term(term):
    assert isinstance(term, mm.util.Term)

    assert isinstance(term._allowed_attributes, list)
    assert len(term._allowed_attributes) > 0

    if isinstance(term, mm.energy.energyterm.EnergyTerm):
        assert isinstance(getattr(mm, term._container_class)(), mm.Energy)
    else:
        assert isinstance(getattr(mm, term._container_class)(), mm.Dynamics)

    assert term == term
    assert not term != term
    assert term != '5'

    container = getattr(mm, term._container_class)()
    assert len(container) == 0
    container += term
    assert len(container) == 1
    assert term in container

    # neutral element for addition
    assert container + getattr(mm, term._container_class)() == container

    assert getattr(container, term.name) == term
    assert term.name in dir(container)

    container -= term
    assert len(container) == 0
    assert term not in container

    # Try to add two terms of the same type.
    with pytest.raises(ValueError):
        container = term + term

    assert isinstance(repr(term), str)
    assert re.search(r'^.+\(.*\)$', repr(term))

    assert isinstance(term._repr_latex_(), str)
    assert re.search(r'^\$.+\$$', term._repr_latex_())

    assert isinstance(term.name, str)
    assert re.search(r'\w+', term.name)


def check_container(container):
    assert isinstance(container, mm.util.Container)
    assert isinstance(container._terms, list)

    assert isinstance(container._term_class, mm.util.Term)

    assert isinstance(len(container), int)
    assert len(container) >= 0

    assert isinstance(iter(container), types.GeneratorType)
    assert list(container) == container._terms

    assert container == container
    assert not container != container
    assert container != '5'

    assert isinstance(dir(term), list)

    assert isinstance(iter(container), types.GeneratorType)
    assert list(container) == container._terms

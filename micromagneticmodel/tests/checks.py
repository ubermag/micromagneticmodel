import types
import pytest
import micromagneticmodel as mm


def check_term(term):
    assert isinstance(term, mm.util.Term)

    assert isinstance(term._allowed_attributes, list)
    assert len(term._allowed_attributes) > 0

    assert isinstance(getattr(mm, term._termscontainer_class)(),
                      mm.util.TermsContainer)

    assert term == term
    assert term != '5'
    assert not term != term

    assert isinstance(dir(term), list)

    termsum = getattr(mm, term._termscontainer_class)()
    termsum += term
    assert len(termsum) == 1
    assert term in termsum

    assert isinstance(iter(termsum), types.GeneratorType)
    assert list(termsum) == termsum._terms

    # neutral element for addition
    assert termsum + getattr(mm, term._termscontainer_class)() == termsum

    assert getattr(termsum, term.name) == term
    assert term.name in dir(termsum)

    termsum -= term
    assert len(termsum) == 0
    assert term not in termsum

    # Try to add two terms of the same type.
    with pytest.raises(ValueError):
        termsum = term + term

    assert isinstance(repr(term), str)

    assert isinstance(term._repr_latex_(), str)
    assert term._repr_latex_().startswith('$')
    assert term._repr_latex_().endswith('$')

    assert isinstance(term.name, str)

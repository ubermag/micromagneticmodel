import abc


class Container(metaclass=abc.ABCMeta):
    """Container abstract class.

    Container can be initialised with a list of either energy or
    dynamics terms.

    Parameters
    ----------
    terms : list, optional

        A list of either energy or dynamics terms. Defaults to ``None``. If
        ``terms`` is not passed, an empty container is initialised.

    Examples
    --------
    1. Defining energy terms container.

    >>> import micromagneticmodel as mm
    ...
    >>> terms = [mm.Exchange(A=1e-12), mm.Demag()]
    >>> energy = mm.Energy(terms=terms)
    >>> len(energy)  # the number of terms
    2

    2. Defining dynamics terms container, by adding terms individually.

    >>> dynamics = mm.Dynamics()
    >>> len(dynamics)
    0
    >>> dynamics += mm.Precession(gamma0=mm.consts.gamma0)
    >>> len(dynamics)
    1
    >>> dynamics += mm.Damping()
    >>> len(dynamics)
    2

    """

    def __init__(self, terms=None):
        self._terms = list()
        if terms is not None:
            for term in terms:
                # all necessary checks are done by the + operator
                self._terms = (self + term)._terms

    @property
    @abc.abstractmethod
    def _term_class(self):
        """The class of terms which can be added to ``Container``."""
        pass  # pragma: no cover

    def __len__(self):
        """The number of terms in the container.

        Returns
        -------
        int

            The number of terms.

        Examples
        --------
        1. Getting the number of terms in the container.

        >>> import micromagneticmodel as mm
        ...
        >>> dynamics = mm.Dynamics()
        >>> len(dynamics)
        0
        >>> dynamics += mm.Precession(gamma0=mm.consts.gamma0)
        >>> len(dynamics)
        1
        >>> dynamics += mm.Damping(alpha=0.2)
        >>> len(dynamics)
        2

        """
        return len(self._terms)

    def __iter__(self):
        """Generator yielding all terms in the container.

        Yields
        ------
        micromagneticmodel.abstract.Term

            Term in the container.

        Examples
        --------
        1. Iterating energy terms container.

        >>> import micromagneticmodel as mm
        ...
        >>> terms = [mm.Exchange(A=1e-12), mm.Demag()]
        >>> energy = mm.Energy(terms=terms)
        >>> for term in energy:
        ...     print(term)
        Exchange(A=1e-12)
        Demag()

        """
        for term in self._terms:
            yield term

    def __contains__(self, item):
        """Determine whether a term of the same type as ``item`` is in the
        container.

        Parameters
        ----------
        item : micromagneticmodel.abstract.Term

            Energy or dynamics term.

        Returns
        -------
        bool

            ``True`` if term of the same type as ``item`` is in the container
            and ``False`` otherwise.

        Example
        -------
        1. Checking if the container contains a term.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> demag = mm.Demag()
        >>> energy = mm.Energy(terms=[exchange, demag])
        >>> exchange in energy
        True
        >>> demag in energy
        True
        >>> mm.Zeeman(H=(0, 0, 1)) in energy
        False
        >>> # Looks for a term of the same type only.
        >>> mm.Exchange(A=5e-11) in energy
        True

        """
        for term in self:
            if term.name == item.name:
                return True
        else:
            return False

    def __getattr__(self, attr):
        """Accessing an individual term from the container.

        Each term in the container can be accessed using its ``name``. The name
        of the term is the same as the name of its class in lowercase. For
        example, for ``micromagneticmodel.DMI``, the name is ``dmi``.

        Parameters
        ----------
        attr : str

            The name of the term.

        Returns
        -------
        micromagneticmodel.Term

            Term from the container.

        Raises
        ------
        AttributeError

            If ``attr`` is not in the container.

        Examples
        --------
        1. Accessing individual terms from the container.

        >>> import micromagneticmodel as mm
        ...
        >>> dynamics = mm.Dynamics()
        >>> dynamics += mm.Precession(gamma0=500)
        >>> dynamics += mm.Damping(alpha=0.2)
        >>> dynamics.precession
        Precession(gamma0=500)
        >>> dynamics.damping
        Damping(alpha=0.2)
        >>> dynamics.stt
        Traceback (most recent call last):
        ...
        AttributeError: ...

        """
        for term in self:
            if term.name == attr:
                return term
        else:
            msg = f"Object has no attribute {attr}."
            raise AttributeError(msg)

    def __dir__(self):
        """Extension of the ``dir(self)`` list.

        Adds the names of terms in the container to the list of attributes.

        Returns
        -------
        list

            Avalilable attributes.

        Examples
        --------
        1. Checking the list of attributes using ``dir()``.

        >>> import micromagneticmodel as mm
        ...
        >>> dynamics = mm.Dynamics()
        >>> 'precession' in dir(dynamics)
        False
        >>> 'damping' in dir(dynamics)
        False
        >>> dynamics += mm.Precession(gamma0=mm.consts.gamma0)
        >>> 'precession' in dir(dynamics)
        True
        >>> dynamics += mm.Damping(alpha=0.2)
        >>> 'damping' in dir(dynamics)
        True

        """
        dirlist = dir(self.__class__)
        for term in self:
            dirlist.append(term.name)

        return dirlist

    def __eq__(self, other):
        """Relational operator ``==``.

        Two containers are considered to be equal if they have the same number
        of terms and the same types of terms in them.

        Parameters
        ----------
        other : micromagneticmodel.TermsContainer

            Second operand.

        Returns
        -------
        bool

            ``True`` if two container have the same number of terms and the
            same types of terms in them and ``False`` otherwise.

        Examples
        --------
        1. Comparing term containers.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> demag = mm.Demag()
        >>> energy1 = mm.Energy(terms=[exchange, demag])
        >>> energy2 = mm.Energy(terms=[demag])
        >>> energy1 == energy1
        True
        >>> energy1 == energy2
        False
        >>> energy1 != energy2
        True

        """
        if not isinstance(other, self.__class__):
            return False
        if len(self) == len(other) and all(term in self for term in other):
            return True
        else:
            return False

    def __add__(self, other):
        """Binary ``+`` operator.

        It can be applied only between ``micromagneticmodel.abstract.Term`` or
        ``micromagneticmodel.abstract.TermsContainer`` objects. If the term
        with the same name is already present in the container ``ValueError``
        is raised.

        Parameters
        ----------
        other : micromagneticmodel.abstract.Term, TermsContainer

            Second operand.

        Returns
        -------
        micromagneticmodel.abstract.TermContainer

            Resulting container.

        Raises
        ------
        TypeError

            If the operator cannot be applied.

        ValueError

            If the term with the same name is already present in the container.

        Examples
        --------
        1. Binary operator ``+``.

        >>> import micromagneticmodel as mm
        ...
        >>> dynamics = mm.Dynamics()
        >>> dynamics += mm.Precession(gamma0=mm.consts.gamma0)
        >>> dynamics += mm.Damping(alpha=0.2)
        >>> len(dynamics)
        2

        """
        result = self.__class__()
        for term in self:
            result._terms.append(term)

        if isinstance(other, self._term_class):
            if other in result:
                msg = f"Cannot have two {other.__class__} terms in the container."
                raise ValueError(msg)
            result._terms.append(other)
        elif isinstance(other, self.__class__):
            for term in other:
                result += term
        else:
            msg = f"Unsupported operand type(s) for +: {type(self)} and {type(other)}."
            raise TypeError(msg)

        return result

    def __sub__(self, other):
        """Binary ``-`` operator.

        It can be applied only between
        ``micromagneticmodel.abstract.TermsContainer`` and
        ``micromagneticmodel.abstract.Term``. It removes the term with the same
        name from the container.

        Parameters
        ----------
        other : micromagneticmodel.abstract.Term

            Second operand.

        Returns
        -------
        micromagneticmodel.abstract.TermContainer

            Resulting container.

        Raises
        ------
        TypeError

            If the operator cannot be applied.

        ValueError

            If the term with the same name is not present in the container.

        Examples
        --------
        1. Binary operator ``-``.

        >>> import micromagneticmodel as mm
        ...
        >>> dynamics = mm.Dynamics()
        >>> dynamics += mm.Precession(gamma0=mm.consts.gamma0)
        >>> len(dynamics)
        1
        >>> damping = mm.Damping(alpha=0.2)
        >>> dynamics += damping
        >>> len(dynamics)
        2
        >>> dynamics -= damping
        >>> len(dynamics)
        1
        >>> damping in dynamics
        False

        """
        result = self.__class__()
        for term in self:
            result._terms.append(term)

        if isinstance(other, self._term_class):
            if other not in result:
                msg = f"Term {other.__class__} not in {self.__class__}."
                raise ValueError(msg)
            for term in result:
                if term.name == other.name:
                    result._terms.remove(term)
        elif isinstance(other, self.__class__):
            for term in other:
                result -= term
        else:
            msg = f"Unsupported operand type(s) for +: {type(self)} and {type(other)}."
            raise TypeError(msg)

        return result

    def __repr__(self):
        """Representation string.

        Returns
        -------
        str

            Representation string.

        Examples
        --------
        1. Getting representation string.

        >>> import micromagneticmodel as mm
        ...
        >>> exchange = mm.Exchange(A=1e-12)
        >>> demag = mm.Demag()
        >>> energy = exchange + demag
        >>> repr(energy)
        'Exchange(A=1e-12) + Demag()'

        """
        if len(self) == 0:
            return f"{self.__class__.__name__}()"
        else:
            return " + ".join([repr(term) for term in self])

    def _repr_latex_(self):
        """ "LaTeX representation method, rendered inside Jupyter. This method
        has the priority over ``__repr__`` in Jupyter.

        Returns
        -------
        str

            LaTeX representation string.

        Examples
        --------
        1. Getting LaTeX representation string.

        >>> import micromagneticmodel as mm
        ...
        >>> zeeman = mm.Zeeman(H=(100, 0, 0))
        >>> energy = mm.Energy()
        >>> energy += zeeman
        >>> energy._repr_latex_()
        '$-\\\\mu_{0}M_\\\\text{s} \\\\mathbf{m} \\\\cdot \\\\mathbf{H}$'
        >>> # energy  # inside Jupyter

        """
        reprlatex = ""
        if not self._terms:
            reprlatex += "0"
        else:
            for term in self:
                termlatex = term._reprlatex
                if not reprlatex:
                    # Adding the first term. No leading +.
                    reprlatex += termlatex
                else:
                    if not termlatex.startswith("-"):
                        # Is it the first term added to the sum? No leading +.
                        reprlatex += f"+ {termlatex}"
                    else:
                        reprlatex += termlatex

        return f"${reprlatex}$"

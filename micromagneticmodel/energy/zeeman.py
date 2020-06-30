import ubermagutil as uu
import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(H=ts.Parameter(descriptor=ts.Vector(size=3),
                              otherwise=df.Field),
               wave=ts.Subset(sample_set={'sin', 'sinc'}, unpack=False),
               f=ts.Scalar(positive=True),
               t0=ts.Scalar())
class Zeeman(EnergyTerm):
    """Zeeman energy term.

    .. math::

        w = -\\mu_{0}M_\\text{s} \\mathbf{m} \\cdot \\mathbf{H}

    Zeeman energy term allows defining time-dependent as well as
    time-independent external magnetic field. If only external magnetic field
    ``H`` is passed, a time-constant field is defined. On the other hand, in
    order to define a time-dependent field, ``wave`` must be passed as a
    string. ``wave`` can be either ``'sine'`` or ``'sinc'``. If time-dependent
    external magnetic field is defined, apart from ``wave``, ``f`` and ``t0``
    must be passed. For ``wave='sine'``, energy density is:

    .. math::

        w = -\\mu_{0}M_\\text{s} \\mathbf{m} \\cdot \\mathbf{H} \\sin[2\\pi
        f(t-t_{0})]

    whereas for ``wave='sinc'``, the energy density is:

    .. math::

        w = -\\mu_{0}M_\\text{s} \\mathbf{m} \\cdot \\mathbf{H}
        \\text{sinc}[2\\pi f(t-t_{0})]

    and ``f`` is a cut-off frequency.

    Parameters
    ----------
    H : (3,) array_like, dict, discretisedfield.Field

        If a single length-3 array_like (tuple, list, ``numpy.ndarray``) is
        passed, which consists of ``numbers.Real``, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``H={'region1': (0, 0, 3e6), 'region2': (0, 0,
        -3e6)}`` (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

    wave : str

        For a time dependent field, either ``'sine'`` or ``'sinc'`` is passed.

    f : numbers.Real

        (Cut-off) frequency in Hz.

    t0 : numbers.Real

        Time for adjusting the phase (time-shift) of a wave.

    Examples
    --------
    1. Defining the Zeeman energy term using a vector.

    >>> import micromagneticmodel as mm
    ...
    >>> zeeman = mm.Zeeman(H=(0, 0, 1e6))

    2. Defining the Zeeman energy term using dictionary.

    >>> zeeman = mm.Zeeman(H={'region1': (0, 0, 1e6), 'region2': (0, 0, -1e6)})

    3. Defining the Zeeman energy term using ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 10e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 10))
    >>> H = df.Field(mesh, dim=3, value=(1e6, -1e6, 0))
    >>> zeeman = mm.Zeeman(H=H)

    4. Defining the Zeeman energy term using a vector which changes as a sine
    wave.

    >>> zeeman = mm.Zeeman(H=(0, 0, 1e6), wave='sin', f=1e9, t0=0)

    5. An attempt to define the Zeeman energy term using a wrong value.

    >>> zeeman = mm.Zeeman(H=(0, -1e7))  # length-2 vector
    Traceback (most recent call last):
    ...
    ValueError: ...

    """
    _allowed_attributes = ['H', 'wave', 'f', 't0']

    @property
    def _reprlatex(self):
        if self.wave == 'sin':
            return (r'-\mu_{0}M_\text{s} \mathbf{m}'
                    r'\cdot \mathbf{H} \sin[2 \pi f (t-t_{0})]')
        elif self.wave == 'sinc':
            return (r'-\mu_{0}M_\text{s} \mathbf{m} \cdot \mathbf{H}\, '
                    r'\text{sinc}[2 \pi f (t-t_{0})]')
        else:
            return r'-\mu_{0}M_\text{s} \mathbf{m} \cdot \mathbf{H}'

    def effective_field(self, m):
        raise NotImplementedError

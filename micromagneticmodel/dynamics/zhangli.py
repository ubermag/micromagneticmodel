import collections
import numbers

import discretisedfield as df
import numpy as np
import ubermagutil as uu
import ubermagutil.typesystem as ts

from .dynamicsterm import DynamicsTerm


class Scalar_Vector3(ts.Descriptor):
    """custom type for Zhand-Li current density u.""
    def __set__(self, instance, value):
        if not isinstance(value, (numbers.Real, tuple, list, np.ndarray, df.Field)):
            raise TypeError("Cannot set {self.name} with {type(value)}.")
        if isinstance(value, numbers.Real):
            pass
        elif isinstance(value, df.Field):
            if value.nvdim not in (1, 3):
                raise ValueError("Cannot set {self.name} with {value.nvdim=}.")
        else:
            if not all(isinstance(elem, numbers.Real) for elem in value):
                raise ValueError(
                    "Can only set {self.name} with elements of type numbers.Real."
                )
        super().__set__(instance, value)


@uu.inherit_docs
@ts.typesystem(
    u=Scalar_Vector3(),
    beta=ts.Scalar(),
    func=ts.Typed(expected_type=collections.abc.Callable),
    dt=ts.Scalar(positive=True),
    tcl_strings=ts.Dictionary(
        key_descriptor=ts.Subset(
            sample_set=("script", "script_args", "script_name"), unpack=False
        ),
        value_descriptor=ts.Typed(expected_type=str),
    ),
)
class ZhangLi(DynamicsTerm):
    r"""Zhang-Li spin transfer torque dynamics term.

    .. math::

        \frac{\text{d}\mathbf{m}}{\text{d}t} = -\frac{1+\alpha\beta}{1+\alpha^{2}}
            \mathbf{m} \times (\mathbf{m} \times (\mathbf{u} \cdot \boldsymbol\nabla)
            \mathbf{m}) - \frac{\beta - \alpha}{1+\alpha^{2}} \mathbf{m} \times
            (\mathbf{u} \cdot \boldsymbol\nabla)\mathbf{m}

    A time-dependent current can be specified by providing a time-dependent
    pre-factor that is used to multiply ``u``. The time-dependence can either
    be specified by providing a callable ``func`` that is evaluated at time
    steps ``dt`` or by passing a dictionary ``tcl_strings`` of tcl strings that
    are written to the mif file.

    Parameters
    ----------
    beta : numbers.Real

        A single scalar value can be passed.

    u : number.Real, array-like, discretisedfield.Field

        Spin-drift velocity in m/s. If a scalar value or ``Field`` with
        ``nvdim==1`` is passed, the current is assumed to flow in x direction. A vector
        or a ``Field`` with ``nvdim==3`` can be used to specify arbitrary current
        direction.

    func : callable, optional

        Callable to define arbitrary time-dependence, multiplies ``u``. Called
        at times that are multiples of ``dt``. Must return a single number.

    dt : numbers.Real, optional (required for ``func``)

        Time steps in seconds to evaluate callable ``func`` at.

    tcl_strings : dict, optional

        Dictionary of ``tcl`` strings to be included into the ``mif`` file for
        more control over specific time-dependencies. Must contain the
        following keys: ``script``, ``script_args``, and ``script_name``. Refer
        to the OOMMF documentation for more details (behaves similar to
        Slonczewski current/Oxs_SpinXferEvolve:
        https://math.nist.gov/oommf/doc/userguide20a3/userguide/Standard_Oxs_Ext_Child_Clas.html#SX).

    Examples
    --------
    1. Defining the Zhang-Li dynamics term using scalar.

    >>> import micromagneticmodel as mm
    ...
    >>> zhangli = mm.ZhangLi(beta=0.01, u=5e6)

    2. Defining the Zhang-Li dynamics term using ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 5e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 5))
    >>> beta = 0.012
    >>> u = df.Field(mesh, nvdim=1, value=1e5)
    >>> zhangli = mm.ZhangLi(beta=beta, u=u)

    3. Defining a sinusoidal decaying current.

    >>> import micromagneticmodel as mm
    >>> import numpy as np
    ...
    >>> def sin_wave(t):
    ...     omega = 2 * np.pi / 1e-9
    ...     return np.sin(omega * t)
    >>> zhangli = mm.ZhangLi(beta=0.01, u=5e6, func=sin_wave, dt=1e-13)

    4. An attempt to define the Zhang-Li dynamics term using a wrong value
       (here using a vector ``u`` where a scalar value is required).

    >>> zhangli = mm.ZhangLi(beta=-1, u=(0, 0, 1))  # vector value
    Traceback (most recent call last):
    ...
    TypeError: ...

    """

    _allowed_attributes = ["u", "beta", "func", "dt", "tcl_strings"]

    _reprlatex = (
        r"-\frac{1+\alpha\beta}{1+\alpha^{2}} \mathbf{m} \times "
        r"(\mathbf{m} \times (\mathbf{u} \cdot \boldsymbol\nabla)\mathbf{m}) - "
        r"\frac{\beta - \alpha}{1+\alpha^{2}} \mathbf{m} \times "
        r"(\mathbf{u} \cdot \boldsymbol\nabla)\mathbf{m}"
    )

    def dmdt(self, m, Heff):
        raise NotImplementedError

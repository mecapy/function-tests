"""
Platform test fixtures — merged noop + workflow fixtures.

Functions:

- ``noop``       : returns immediately with ``result=0`` (FRO-perf-01 baseline)
- ``fail``       : always raises ``RuntimeError`` (FRO-exec-04, FRO-jobs-06)
- ``scale``      : multiply a Force by a dimensionless factor (workflow BDD)
- ``bolt_area``  : compute bolt nominal stress area from a struct input
                   (workflow BDD struct InputNode test)

All handlers are deterministic and pure so the BDD suite can assert exact
terminal outputs without mocking.
"""

import math
from typing import Any


def noop(inputs: dict[str, Any]) -> dict[str, Any]:
    """No-operation function — returns immediately.

    Parameters
    ----------
    inputs : dict
        Any input (ignored)

    Returns
    -------
    dict
        result : int
            Always 0
    """
    return {"result": 0}


def fail(inputs: dict[str, Any]) -> dict[str, Any]:
    """Always-failing function used by failure-path tests.

    Raises
    ------
    RuntimeError
        Unconditionally, so the execution job is marked as ``failed`` and
        the UI can surface the error card.
    """
    raise RuntimeError("Intentional failure for mecapy-tests.fail test fixture")


def scale(inputs: dict[str, Any]) -> dict[str, Any]:
    """Multiply the ``force`` by the ``factor`` scalar.

    Parameters
    ----------
    inputs : dict
        force : float
            Source force in Newtons.
        factor : float
            Dimensionless scaling factor.

    Returns
    -------
    dict
        output : float
            ``force * factor`` in Newtons.
    """
    value = float(inputs["force"])
    factor = float(inputs["factor"])
    return {"output": value * factor}


def bolt_area(inputs: dict[str, Any]) -> dict[str, Any]:
    """Compute the stress area of a bolt from a struct input.

    Mirrors the e25-030-1 style: the InputNode carries a dict with named
    typed fields, the function reads the fields by name.

    Parameters
    ----------
    inputs : dict
        bolt : dict
            d : float (Length, mm) — nominal diameter
            p : float (Length, mm) — thread pitch

    Returns
    -------
    dict
        area : float (Area, mm²) — pi/4 * (d - 0.9382 * p)^2
    """
    bolt = inputs["bolt"]
    d = float(bolt["d"])
    p = float(bolt["p"])
    effective = d - 0.9382 * p
    return {"area": math.pi / 4.0 * effective * effective}

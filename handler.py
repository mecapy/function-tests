"""
Platform test fixtures — merged noop + workflow fixtures.

Functions:

- ``noop``       : returns immediately with ``result=0`` (FRO-perf-01 baseline)
- ``fail``       : always raises ``RuntimeError`` (FRO-exec-04, FRO-jobs-06)
- ``scale``      : multiply a Force by a dimensionless factor (workflow BDD)
- ``bolt_area``  : compute bolt nominal stress area from a struct input
                   (workflow BDD struct InputNode test)
- ``file_info``  : read a File input and return size/sha256/line_count
                   (FRO-type-07 + SDK File upload helper end-to-end target)

All handlers are deterministic and pure so the BDD suite can assert exact
terminal outputs without mocking.
"""

import hashlib
import math
from pathlib import Path
from typing import Any


def noop(**_inputs: Any) -> dict[str, Any]:
    """No-operation function — returns immediately.

    Returns
    -------
    dict
        result : int
            Always 0
    """
    return {"result": 0}


def fail(**_inputs: Any) -> dict[str, Any]:
    """Always-failing function used by failure-path tests.

    Raises
    ------
    RuntimeError
        Unconditionally, so the execution job is marked as ``failed`` and
        the UI can surface the error card.
    """
    raise RuntimeError("Intentional failure for mecapy-tests.fail test fixture")


def scale(force: float, factor: float) -> dict[str, Any]:
    """Multiply ``force`` by ``factor``.

    Parameters
    ----------
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
    return {"output": float(force) * float(factor)}


def bolt_area(bolt: dict[str, Any]) -> dict[str, Any]:
    """Compute the stress area of a bolt from a struct input.

    Mirrors the e25-030-1 style: the InputNode carries a dict with named
    typed fields, the function reads the fields by name.

    Parameters
    ----------
    bolt : dict
        d : float (Length, mm) — nominal diameter
        p : float (Length, mm) — thread pitch

    Returns
    -------
    dict
        area : float (Area, mm²) — pi/4 * (d - 0.9382 * p)^2
    """
    d = float(bolt["d"])
    p = float(bolt["p"])
    effective = d - 0.9382 * p
    return {"area": math.pi / 4.0 * effective * effective}


def file_info(file: Path) -> dict[str, Any]:
    """Read an input File and return its size, sha256, and line count.

    Used as the canonical end-to-end target for File upload — both the
    backend ``POST /uploads`` route (FRO-runtime-02) and the SDK's
    ``Function.submit(file=Path(...))`` auto-upload helper.

    Parameters
    ----------
    file : Path
        File input materialised by the runner under
        ``/workspace/in/files/<var>.<ext>``. The runner passes a
        :class:`pathlib.Path` per FRO-runtime-02.

    Returns
    -------
    dict
        size_bytes : int  — total byte size of the file content.
        sha256     : str  — hex digest of the SHA-256 hash.
        line_count : int  — number of newline-terminated lines.
    """
    content = file.read_bytes()
    return {
        "size_bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "line_count": content.count(b"\n"),
    }

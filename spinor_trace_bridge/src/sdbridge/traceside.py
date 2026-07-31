"""Access to the frozen trace implementation, by public interface only.

The bridge is a third package.  It is allowed to import `sdinv`, but it must not
restate or re-derive anything `sdinv` computes -- in particular the Hodge star,
the self-dual projector and the invariant registry are used exactly as the
frozen implementation defines them.  If this module ever grows a formula, that
is a bug.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


def _trace_repo_root() -> Path:
    """The repository root, found by walking up from this file."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "src" / "sdinv" / "forms.py").exists():
            return parent
    raise RuntimeError(
        "could not locate the trace repository root: expected an ancestor "
        "directory containing src/sdinv/forms.py")


ROOT = _trace_repo_root()
_SRC = str(ROOT / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

forms = importlib.import_module("sdinv.forms")
modp = importlib.import_module("sdinv.modp")
contract = importlib.import_module("sdinv.contract")
invariant_registry = importlib.import_module("sdinv.invariant_registry")


def load_registry():
    """The exact committed invariant registry through degree 10."""
    return invariant_registry.load_verified_registry(ROOT)

"""Choose post-freeze points and a prime absent from all scanned frozen content."""
from pathlib import Path
import gzip
import hashlib
import io
import json
import math
import os
import random
import re
import secrets
import subprocess
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "frozen-checkout"
seen = set()
records = []


def inspect(name, payload, depth=0):
    records.append({"name": name, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    seen.update(int(m) for m in re.findall(rb"(?<![0-9])[0-9]{2,5}(?![0-9])", payload))
    if depth < 4 and payload[:2] == b"\x1f\x8b":
        inspect(name + "::gzip", gzip.decompress(payload), depth + 1)
    if depth < 4 and payload[:4] == b"PK\x03\x04":
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            for entry in archive.infolist():
                if not entry.is_dir():
                    inspect(name + "::" + entry.filename, archive.read(entry), depth + 1)


for rel in subprocess.check_output(["git", "ls-files", "-z"], cwd=REPO).decode().split("\0"):
    if rel:
        path = REPO / rel
        if path.is_symlink():
            inspect(rel + "::symlink-target-text", os.readlink(path).encode())
        else:
            inspect(rel, path.read_bytes())
prime = next(p for p in range(50001, 65522, 2)
             if p not in seen and all(p % d for d in range(2, math.isqrt(p) + 1)))
cells = []
for p in [prime, 32749]:
    seed = secrets.randbits(64)
    rng = random.Random(seed)
    coordinates = [rng.randrange(p) for _ in range(126)]
    direction = [rng.randrange(p) for _ in range(126)]
    cells.append({"prime": p, "seed": seed, "coordinates": coordinates,
                  "direction": direction, "generator": "Python random.Random(seed); 126 coordinates then 126 direction residues"})
data = {"frozen_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
        "created_unix": time.time(), "new_prime": prime,
        "new_prime_selection": "First prime >=50001 and <=65521 whose decimal integer token occurs in none of the frozen tracked raw files or recursively expanded gzip/zip members (depth<=4).",
        "scope_limit": "Absence from committed source/artifacts and packaged members; uncommitted or external historical computations cannot be inspected.",
        "scanned_payloads": len(records), "cells": cells}
(ROOT / "root-review/fresh_cells.json").write_text(json.dumps(data, indent=2) + "\n")
(ROOT / "root-review/prime_scan_manifest.json").write_text(json.dumps(records, indent=2) + "\n")
print(json.dumps({"new_prime": prime, "scanned_payloads": len(records), "cells": [{k:c[k] for k in ["prime", "seed"]} for c in cells]}, indent=2))

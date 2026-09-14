#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys

root=Path(__file__).resolve().parents[1]
manifest=root/"SHA256SUMS.txt"
bad=[]
for line in manifest.read_text(encoding="utf-8").splitlines():
    if not line.strip(): continue
    expected, rel=line.split("  ",1)
    p=root/rel
    if not p.is_file():
        bad.append((rel,"MISSING"))
        continue
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if h != expected:
        bad.append((rel,h))
if bad:
    print("CHECKSUM_VALIDATION=FAIL")
    for x in bad: print(x)
    sys.exit(1)
print("CHECKSUM_VALIDATION=PASS")

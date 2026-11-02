"""Reference-reason corpus: loader + validator (docs/definitions.md, section 3).

Every reason must point to a source in sources.csv; `side` is the stance a video giving that reason
typically takes toward the claim. The corpus is deliberately limited, not 'balanced'.
"""
import csv
from pathlib import Path

SIDES = {"strict", "balanced", "alt"}
REF_DIR = Path(__file__).resolve().parents[2] / "data" / "reference"


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load(ref_dir=REF_DIR):
    ref_dir = Path(ref_dir)
    return (_read(ref_dir / "claims.csv"), _read(ref_dir / "reference_reasons.csv"),
            {r["source_id"]: r for r in _read(ref_dir / "sources.csv")})


def reason_ids(reasons, claim_id):
    return [r["reason_id"] for r in reasons if r["claim_id"] == claim_id]


def validate(claims, reasons, sources):
    """Return a list of problems (empty list = corpus is consistent)."""
    problems, seen = [], set()
    claim_ids = {c["claim_id"] for c in claims}
    for r in reasons:
        key = (r["claim_id"], r["reason_id"])
        if key in seen:
            problems.append(f"duplicate reason {key}")
        seen.add(key)
        if r["claim_id"] not in claim_ids:
            problems.append(f"{key}: unknown claim")
        if r["side"] not in SIDES:
            problems.append(f"{key}: bad side {r['side']!r}")
        if r["source_id"] not in sources:
            problems.append(f"{key}: missing source {r['source_id']!r}")
        if not r["reason_en"].strip() or not r["reason_zh"].strip():
            problems.append(f"{key}: empty text")
    for c in claim_ids:
        if len(reason_ids(reasons, c)) < 4:
            problems.append(f"claim {c}: fewer than 4 reasons")
    for s in sources.values():
        if not s["url"].startswith("http"):
            problems.append(f"source {s['source_id']}: no URL")
    return problems

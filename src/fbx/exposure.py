"""Viewpoint-exposure measurement (plan §2, 'Data analysis').

Input rows are dicts with: item_id, t, issue, claim_id, stance, reason, source, status.
status == 'unknown' items are excluded from stance distributions and reported as a proportion.
Entropy / JSD describe concentration and change only; they do not establish harm.
"""
import csv
import math
from collections import Counter

UNKNOWN = "unknown"


def load_labels(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["t"] = int(r["t"])
    return sorted(rows, key=lambda r: r["t"])


def distribution(rows, key="stance"):
    """Normalised distribution over `key`, excluding unknown labels. Returns {} if nothing scored."""
    c = Counter(r[key] for r in rows if r["status"] != UNKNOWN and r[key])
    n = sum(c.values())
    return {k: v / n for k, v in c.items()} if n else {}


def entropy(p):
    """Shannon entropy in bits. Lower = exposure concentrated in fewer stances."""
    return -sum(v * math.log2(v) for v in p.values() if v > 0)


def jsd(p, q):
    """Jensen-Shannon divergence in bits (0..1) against an explicit reference q."""
    keys = set(p) | set(q)
    m = {k: 0.5 * (p.get(k, 0) + q.get(k, 0)) for k in keys}

    def kl(a):
        return sum(a[k] * math.log2(a[k] / m[k]) for k in keys if a.get(k, 0) > 0)

    return 0.5 * kl(p) + 0.5 * kl(q)


def summary(rows, claim_id, reference_reasons=None, min_scored=5):
    """Exposure summary for one claim. Sparse histories stay unscored (returns scored=False)."""
    rs = [r for r in rows if r["claim_id"] == claim_id]
    scored = [r for r in rs if r["status"] != UNKNOWN]
    out = {"claim_id": claim_id, "n_items": len(rs), "n_scored": len(scored),
           "unknown_prop": (1 - len(scored) / len(rs)) if rs else None, "scored": len(scored) >= min_scored}
    if not out["scored"]:
        return out
    p = distribution(rs)
    reasons = {r["reason"] for r in scored if r["reason"]}
    src = Counter(r["source"] for r in scored if r["source"])
    out.update(stance_dist=p, entropy=entropy(p), reasons_seen=sorted(reasons),
               reason_coverage=(len(reasons & set(reference_reasons)) / len(reference_reasons)) if reference_reasons else None,
               top_source_share=(src.most_common(1)[0][1] / sum(src.values())) if src else None)
    return out


def sliding(rows, claim_id, window=10, step=5, reference=None):
    """Per-window entropy and JSD vs `reference` (default: the first window = 'earlier exposure')."""
    rs = [r for r in rows if r["claim_id"] == claim_id]
    out, ref = [], reference
    for s in range(0, max(len(rs) - window + 1, 0), step):
        w = rs[s:s + window]
        p = distribution(w)
        if not p:
            continue
        if ref is None:
            ref = p
        out.append({"start_t": w[0]["t"], "end_t": w[-1]["t"], "entropy": entropy(p), "jsd_vs_ref": jsd(p, ref)})
    return out

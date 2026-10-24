"""Generate SYNTHETIC demo labels so the pipeline can be exercised end-to-end.
Replace data/pilot/*.csv with real annotations; nothing generated here is a finding."""
import csv
import random
import sys
from pathlib import Path

out = Path(__file__).resolve().parents[1] / "data" / "pilot"
rng = random.Random(7)
reasons = {"strict": ["r1", "r2"], "balanced": ["r3", "r4"], "alt": ["r5", "r6"]}
rows = []
for t in range(40):
    w = [0.7, 0.2, 0.1] if t < 20 else [0.85, 0.1, 0.05]            # exposure narrows over time (synthetic)
    st = rng.choices(["strict", "balanced", "alt"], weights=w)[0]
    status = "unknown" if rng.random() < 0.1 else "ok"
    rows.append(dict(item_id=f"v{t:03d}", t=t, issue="parenting", claim_id="strict_only", stance=st,
                     reason=rng.choice(reasons[st]), source=rng.choice(["acctA", "acctA", "acctB", "acctC"]),
                     status=status, provenance="synthetic_demo"))
hdr = list(rows[0])
with open(out / "labels_demo.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, hdr); wr.writeheader(); wr.writerows(rows)
for name, flip in (("annotator_A_demo.csv", 0.0), ("annotator_B_demo.csv", 0.15)):
    with open(out / name, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, ["item_id", "stance", "provenance"]); wr.writeheader()
        for r in rows:
            st = r["stance"]
            if rng.random() < flip:
                st = rng.choice([s for s in reasons if s != st])
            wr.writerow(dict(item_id=r["item_id"], stance=st, provenance="synthetic_demo"))
with open(out / "annotation_template.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["item_id", "t", "issue", "claim_id", "stance", "reason", "source", "status", "evidence_passage_or_timestamp"])
print("wrote demo data to", out, file=sys.stderr)

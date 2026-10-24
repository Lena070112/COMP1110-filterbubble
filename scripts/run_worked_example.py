"""Exposure report for one claim from a labels CSV (default: SYNTHETIC demo)."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fbx import exposure as ex  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--labels", default=str(ROOT / "data/pilot/labels_demo.csv"))
ap.add_argument("--claim", default="strict_only")
ap.add_argument("--ref-reasons", default="r1,r2,r3,r4,r5,r6")
a = ap.parse_args()
rows = ex.load_labels(a.labels)
demo = any(r.get("provenance") == "synthetic_demo" for r in rows)
s = ex.summary(rows, a.claim, a.ref_reasons.split(","))
lines = [f"# Exposure report — claim `{a.claim}`", ""]
if demo:
    lines += ["> **SYNTHETIC DEMO DATA — illustrates the output format only; not a finding.**", ""]
lines += [f"- items: {s['n_items']}, scored: {s['n_scored']}, unknown proportion: {s['unknown_prop']:.0%}"]
if s["scored"]:
    lines += ["- stance distribution: " + ", ".join(f"{k} {v:.0%}" for k, v in sorted(s["stance_dist"].items())),
              f"- entropy: {s['entropy']:.2f} bits (max for 3 stances = 1.58)",
              f"- reason coverage vs reference corpus: {s['reason_coverage']:.0%}  (reasons seen: {', '.join(s['reasons_seen'])})",
              f"- top source share: {s['top_source_share']:.0%}", "", "## Sliding windows (JSD vs first window)", "",
              "| window t | entropy | JSD vs ref |", "|---|---|---|"]
    lines += [f"| {w['start_t']}–{w['end_t']} | {w['entropy']:.2f} | {w['jsd_vs_ref']:.3f} |" for w in ex.sliding(rows, a.claim)]
else:
    lines += ["- too few scored items: left unscored (sparse history)."]
lines += ["", "_Entropy/JSD describe concentration and change only; they do not establish harm or that uniform exposure is ideal._"]
out = ROOT / "out" / "exposure_report.md"
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))

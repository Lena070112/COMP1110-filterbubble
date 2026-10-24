"""Matched-seed policy comparison + a small sensitivity check (label error, user model)."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fbx.sim.run import compare, fmt  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--seeds", type=int, default=20)
a = ap.parse_args()
parts = ["# Toy simulation results", "",
         "> Rule-based recommender + rule-based user on a SYNTHETIC catalogue. Compares policies inside this model only; "
         "no claim about real platforms or users' beliefs. Mean±sd over matched seeds.", ""]
for title, kw in [("Default (label error 0.10, strict affinity 0.8)", {}),
                  ("Sensitivity: label error 0.30", {"label_err": 0.30}),
                  ("Sensitivity: weaker viewing tendency (strict affinity 0.5)", {"strict_affinity": 0.5})]:
    parts += [f"## {title}", "", fmt(compare(range(a.seeds), **kw)), ""]
txt = "\n".join(parts)
(ROOT / "out" / "simulation_results.md").write_text(txt, encoding="utf-8")
print(txt)

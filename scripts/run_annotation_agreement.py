import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fbx import annotation as an  # noqa: E402

pa = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "data/pilot/annotator_A_demo.csv")
pb = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / "data/pilot/annotator_B_demo.csv")
a, b = an.load_by_item(pa), an.load_by_item(pb)
print(f"n={len(set(a) & set(b))}  agreement={an.percent_agreement(a, b):.2f}  kappa={an.cohens_kappa(a, b):.2f}")
for d in an.disagreements(a, b):
    print("disagree:", d)
if "demo" in pa:
    print("(SYNTHETIC demo annotations — format check only)")

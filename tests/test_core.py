import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fbx import annotation as an, exposure as ex  # noqa: E402
from fbx.sim.run import compare  # noqa: E402


def row(t, st, status="ok", claim="c"):
    return dict(item_id=str(t), t=t, issue="i", claim_id=claim, stance=st, reason="r", source="s", status=status)


class T(unittest.TestCase):
    def test_entropy_bounds(self):
        self.assertAlmostEqual(ex.entropy({"a": 1.0}), 0.0)
        self.assertAlmostEqual(ex.entropy({"a": .5, "b": .5}), 1.0)

    def test_jsd(self):
        p = {"a": 1.0}
        self.assertAlmostEqual(ex.jsd(p, p), 0.0)
        self.assertAlmostEqual(ex.jsd({"a": 1.0}, {"b": 1.0}), 1.0)

    def test_unknown_excluded_and_sparse_unscored(self):
        rows = [row(i, "a") for i in range(4)] + [row(9, "b", "unknown")]
        s = ex.summary(rows, "c", min_scored=5)
        self.assertFalse(s["scored"])
        self.assertAlmostEqual(s["unknown_prop"], 0.2)
        self.assertEqual(ex.distribution(rows), {"a": 1.0})

    def test_kappa(self):
        a = {"1": "x", "2": "y", "3": "x", "4": "y"}
        self.assertAlmostEqual(an.cohens_kappa(a, a), 1.0)
        b = {"1": "y", "2": "x", "3": "y", "4": "x"}
        self.assertAlmostEqual(an.cohens_kappa(a, b), -1.0)

    def test_sim_reproducible_and_empty_feed_not_success(self):
        t1, t2 = compare(range(3)), compare(range(3))
        self.assertEqual(t1["none"][0]["strict_share"], t2["none"][0]["strict_share"])
        for r in compare(range(5))["topic_filter"]:
            self.assertTrue(r["violation"])        # blocking the topic empties parenting exposure
            self.assertFalse(r["attained"])


if __name__ == "__main__":
    unittest.main()

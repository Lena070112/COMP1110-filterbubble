import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fbx import corpus  # noqa: E402


class CorpusTests(unittest.TestCase):
    def test_shipped_corpus_is_consistent(self):
        claims, reasons, sources = corpus.load()
        self.assertEqual(corpus.validate(claims, reasons, sources), [])
        self.assertEqual({c["role"] for c in claims}, {"issue 1", "issue 2", "held-out issue"})

    def test_validator_catches_missing_source_and_bad_side(self):
        claims, reasons, sources = corpus.load()
        bad = [dict(r) for r in reasons]
        bad[0]["source_id"], bad[1]["side"] = "S99", "neutral"
        problems = corpus.validate(claims, bad, sources)
        self.assertTrue(any("S99" in p for p in problems))
        self.assertTrue(any("neutral" in p for p in problems))


if __name__ == "__main__":
    unittest.main()

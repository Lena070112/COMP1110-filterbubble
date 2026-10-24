"""Annotation quality: agreement between two independent annotators (plan §2 'measurement quality')."""
import csv
from collections import Counter


def load_by_item(path, field="stance"):
    with open(path, newline="", encoding="utf-8") as f:
        return {r["item_id"]: r[field] for r in csv.DictReader(f)}


def percent_agreement(a, b):
    ids = sorted(set(a) & set(b))
    return sum(a[i] == b[i] for i in ids) / len(ids) if ids else float("nan")


def cohens_kappa(a, b):
    ids = sorted(set(a) & set(b))
    n = len(ids)
    if n == 0:
        return float("nan")
    po = sum(a[i] == b[i] for i in ids) / n
    ca, cb = Counter(a[i] for i in ids), Counter(b[i] for i in ids)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def disagreements(a, b):
    return [(i, a[i], b[i]) for i in sorted(set(a) & set(b)) if a[i] != b[i]]

"""Toy recommender <-> user feedback loop (plan §2 'Simulation').

Everything here is a TRANSPARENT RULE-BASED BASELINE on a synthetic catalogue.
It is a test-bed for comparing intervention policies, NOT evidence about any real platform.
Hidden to policies: user affinities and recommender weights. Observable: slate shown, items watched.
"""
import math
import random

TOPICS = ["parenting", "food", "music", "travel"]
STANCES = ["strict", "balanced", "alt"]            # stance on the claim 'strict discipline is the only way'
REASONS = {"strict": ["r1", "r2"], "balanced": ["r3", "r4"], "alt": ["r5", "r6"]}


def make_catalogue(rng, n=3000):
    items = []
    for i in range(n):
        topic = rng.choices(TOPICS, weights=[0.4, 0.2, 0.2, 0.2])[0]
        if topic == "parenting":
            st = rng.choices(STANCES, weights=[0.5, 0.25, 0.25])[0]
            items.append(dict(id=i, topic=topic, stance=st, reason=rng.choice(REASONS[st]), practical=rng.random() < 0.4))
        else:
            items.append(dict(id=i, topic=topic, stance="na", reason=None, practical=False))
    return items


class User:
    """Rule-based user. `strict_affinity` is the viewing tendency (separate from the adjustment goal)."""

    def __init__(self, rng, strict_affinity=0.8):
        self.rng, self.aff = rng, {"strict": strict_affinity, "balanced": 0.5, "alt": 0.5, "na": 0.4}
        self.topic_int = {"parenting": 0.8, "food": 0.4, "music": 0.4, "travel": 0.4}

    def watches(self, it):
        p = 0.15 + 0.35 * self.topic_int[it["topic"]] + 0.3 * self.aff[it["stance"]] + (0.1 if it["practical"] else 0)
        return self.rng.random() < min(p, 0.95)


class Recommender:
    def __init__(self, rng, items, slate=5, eps=0.1, decay=0.98):
        self.rng, self.items, self.k, self.eps, self.decay = rng, items, slate, eps, decay
        self.topic_w = {t: 1.0 for t in TOPICS}
        self.stance_w = {s: 1.0 for s in STANCES + ["na"]}
        self.blocked_topics, self.filter_stances, self.leak = set(), set(), 0.2
        self.boost = {}          # stance -> multiplicative boost (supplementation / follows)
        self.seen = set()

    def eligible(self, it):
        if it["id"] in self.seen or it["topic"] in self.blocked_topics:
            return False
        if it["stance"] in self.filter_stances and self.rng.random() > self.leak:
            return False
        return True

    def slate(self):
        pool = [it for it in self.items if self.eligible(it)]
        if not pool:
            return []
        out = []
        for _ in range(min(self.k, len(pool))):
            if self.rng.random() < self.eps:
                pick = self.rng.choice(pool)
            else:
                w = [self.topic_w[i["topic"]] * self.stance_w[i["stance"]] * self.boost.get(i["stance"], 1.0)
                     * (1.3 if i["practical"] else 1.0) for i in pool]
                pick = self.rng.choices(pool, weights=w)[0]
            pool.remove(pick)
            out.append(pick)
        self.seen.update(i["id"] for i in out)
        return out

    def update(self, it, watched):
        for d in (self.topic_w, self.stance_w):
            for k in d:
                d[k] = 1.0 + (d[k] - 1.0) * self.decay          # decaying memory
        if watched:
            self.topic_w[it["topic"]] *= 1.10
            self.stance_w[it["stance"]] *= 1.05

    def not_interested(self, it):
        self.stance_w[it["stance"]] *= 0.7
        self.topic_w[it["topic"]] *= 0.97                       # platform may over-generalise to the topic

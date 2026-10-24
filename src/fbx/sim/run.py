"""Matched-seed comparison of policies: same catalogue + same random stream per seed."""
import random
import statistics as st

from .env import Recommender, User, make_catalogue, REASONS
from .policies import ALL


def run_one(policy_cls, seed, horizon=120, stop_at=80, budget=20, label_err=0.1, strict_affinity=0.8):
    rng = random.Random(seed)
    items = make_catalogue(rng)
    user, rec = User(random.Random(seed + 1), strict_affinity), Recommender(random.Random(seed + 2), items)
    lab_rng, pol, left = random.Random(seed + 3), policy_cls(), budget

    def label_fn(it):   # noisy 'report' label: observable to the policy, truth is hidden
        if it["stance"] == "na" or lab_rng.random() > label_err:
            return it["stance"]
        return lab_rng.choice([s for s in ("strict", "balanced", "alt") if s != it["stance"]])

    exp = []   # parenting exposures: (t, stance, practical, reason)
    for t in range(horizon):
        shown = rec.slate()
        if t < stop_at and left > 0:
            left -= pol.act(t, shown, rec, label_fn, left)
        for it in shown:
            w = user.watches(it)
            rec.update(it, w)
            if it["topic"] == "parenting":
                exp.append((t, it["stance"], it["practical"], it["reason"], w))
    return dict(exp=exp, effort=budget - left, stop_at=stop_at)


def metrics(res, base, min_retention=0.7):
    def strict_share(e):
        return sum(x[1] == "strict" for x in e) / len(e) if e else float("nan")

    e, b = res["exp"], base["exp"]
    post = [x for x in e if x[0] >= res['stop_at']]
    ret = len([x for x in e if x[2]]) / max(len([x for x in b if x[2]]), 1)
    s, sb = strict_share(e), strict_share(b)
    empty = len(e) == 0                                                # empty feed can never count as success
    attained = (not empty) and s <= 0.5 * sb and ret >= min_retention
    return dict(strict_share=s, retention=ret, effort=res["effort"], reasons=len({x[3] for x in e if x[3]}),
                recurrence=strict_share(post) if post else float("nan"), violation=empty or ret < min_retention,
                attained=attained)


def compare(seeds=range(20), **kw):
    table = {}
    for seed in seeds:
        base = run_one(ALL[0], seed, **kw)
        for P in ALL:
            res = base if P is ALL[0] else run_one(P, seed, **kw)
            table.setdefault(P.name, []).append(metrics(res, base))
    return table


def fmt(table):
    def ms(rows, k):
        v = [r[k] for r in rows if r[k] == r[k]]
        return (st.mean(v), st.pstdev(v)) if v else (float("nan"), float("nan"))

    lines = ["| policy | strict share | retention | effort | reasons seen | recurrence | violation | goal attained |",
             "|---|---|---|---|---|---|---|---|"]
    for name, rows in table.items():
        c = [f"{ms(rows, k)[0]:.2f}±{ms(rows, k)[1]:.2f}" for k in ("strict_share", "retention", "effort", "reasons", "recurrence")]
        lines.append(f"| {name} | " + " | ".join(c) +
                     f" | {sum(r['violation'] for r in rows)/len(rows):.0%} | {sum(r['attained'] for r in rows)/len(rows):.0%} |")
    return "\n".join(lines)

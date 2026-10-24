# Keeping the Topic, Widening the View — analysis & simulation framework

COMP1110 group project (2026/27 Sem 1). Code here supports the project's question: can short-video users reduce a
particular claim or explore missing reasons **within an issue they still follow**, while retaining wanted
information, and at what effort?

> **Status honesty.** This is a scaffold. Anything under `data/pilot/*_demo.csv` is **synthetic** and only exercises
> the pipeline. The simulation is a transparent rule-based **toy**; its numbers compare policies *inside the model*
> and are not evidence about real platforms, users' beliefs or well-being. See `STATUS.md` for what is implemented,
> validated or only proposed.

## Layout
```
src/fbx/exposure.py     stance distribution (unknown excluded), entropy, JSD, reason coverage, source repetition, sliding windows
src/fbx/annotation.py   percent agreement, Cohen's kappa, disagreement list (independent double annotation)
src/fbx/sim/env.py      catalogue, rule-based user, rule-based recommender (relevance + feedback, exploration, decaying memory)
src/fbx/sim/policies.py none / topic filter / negative feedback / selective filter + supplement / search-follow
src/fbx/sim/run.py      matched-seed comparison; goal attainment, retention, effort, recurrence, constraint violations
scripts/                run_worked_example.py, run_annotation_agreement.py, run_simulation.py, make_demo_data.py
tests/                  unit tests (python -m unittest discover -s tests)
data/pilot/             annotation_template.csv + synthetic demo files
docs/                   notes (add annotation protocol, issue/claim definitions here)
```

## Run (Python 3.9+, standard library only)
```
python scripts/run_worked_example.py          # -> out/exposure_report.md
python scripts/run_annotation_agreement.py A.csv B.csv
python scripts/run_simulation.py --seeds 20   # -> out/simulation_results.md
python -m unittest discover -s tests
```
Real workflow: annotate into `data/pilot/annotation_template.csv` format (one CSV per annotator for agreement),
then run the scripts with `--labels`.

## Design choices worth knowing
- `unknown` labels are excluded from stance distributions and reported as a proportion; histories with fewer than
  5 scored items stay unscored; an empty feed can never count as goal attainment.
- Policies only see observable records (the shown slate + a noisy report label), never hidden user affinities or
  recommender weights. The first slate is shown before a policy's first action.
- Same seed => same catalogue and random streams for every policy (matched comparison).
- Not yet implemented: LLM/VLM claim extraction, real datasets (ShortVideo, KuaiRand), learned/LLM user models,
  held-out issue evaluation.

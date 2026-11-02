# Definitions, narrowed research question and corpus (v1, 2 Nov 2026)

Written in response to the feedback that "viewpoint exposure" and "issue corpus" were not clearly defined and that the
research question read more like a UX design prompt than a data science problem. Nothing here has been validated on
real annotations yet; see `STATUS.md`.

## 1. Narrowed research questions
Earlier wording: *can users reduce a claim or explore missing reasons within an issue they still follow, while
retaining wanted information, and at what effort?* This is now split into two measurable questions.

**RQ1 — measurement.** For a fixed claim *c*, can the stance of a short video toward *c* be labelled reliably from its
title and ASR transcript, so that exposure measures (section 2) mean something?
*Success criterion:* Cohen's kappa >= 0.6 between two independent hand annotators on the pilot set of each issue. LLM labels
are reported as precision/recall against the hand-labelled reference. If kappa < 0.6 we use the hand-labelled set only
(as in Project Plan section 4).

**RQ2 — intervention comparison (inside a simulation).** With the same simulated user and recommender (matched seeds),
which of five constrained policies (`none`, `topic_filter`, `negative_feedback`, `selective_filter+supplement`,
`search_follow`) reaches a stated goal, and at what effort? *Goal attained* (as coded in `sim/run.py`) means: share of
claim-endorsing (`strict`) items falls to <= 50% of the no-intervention baseline **and** retention of wanted (practical)
content is >= 70% of baseline. *Effort* = number of user actions spent (budget 20). A feed that ends up empty never counts
as success.

**Hypotheses (falsifiable within the model; not yet tested on anything but the toy):**
- H1: `topic_filter` meets the share target but fails the retention constraint more often than `selective_filter+supplement`.
- H2: The ranking of policies is not invariant to the user model and to the assumed response of the platform to
  "not interested"; we report whether it reverses.
- H3: Exposure measures computed on the two development issues behave the same way on the held-out issue.

**What we do not claim:** causal effects, effects on live platforms, or changes in users' beliefs. We measure what users
are *shown* in data and in simulation, not what they think.

## 2. Definitions
- **Issue** — a topic where short videos routinely take contrasting positions. Two development issues (parenting
  discipline, intensive tutoring) and one held-out issue (bride price); see `data/reference/claims.csv`.
- **Claim** — one sentence stating a position on the issue, with an id (e.g. `strict_only`).
- **Item** — one video, represented by its title and ASR transcript only (no visual content; this is a stated limitation).
- **Stance** (relative to a claim) — `strict` (asserts the claim, presenting it as the only/necessary route), `balanced`
  (accepts it in part, adds conditions or trade-offs), `alt` (rejects it or argues for an alternative), `unknown` (cannot
  be decided from the text). The code names are kept from the first issue and reused for all claims.
- **Reason** — a distinct justification an item gives for its stance, matched to a reference reason id or recorded as
  `new:<text>`.
- **Viewpoint exposure** of a feed window *W* for claim *c*: computed on stance-scored items only (unknown excluded and
  reported as a proportion), as (i) stance distribution *p*, (ii) Shannon entropy *H(p)* in bits, (iii) JSD(*p*, *q*) against
  an explicit reference *q* (default: the first window), (iv) reason coverage = |reasons seen ∩ reference reasons| / |reference reasons|,
  (v) top-source share. Entropy and JSD describe concentration and change; they do not show harm, and uniform exposure is not
  assumed to be ideal. (`src/fbx/exposure.py`)
  *Consistency note:* the code leaves a history unscored below 5 scored items (`min_scored=5`); the revised Project Plan
  section 4 says 10 issue videos per window. The group must pick one number and change code or text.
- **Issue corpus** — the set of items for one issue: videos retrieved from the ShortVideo dataset by keyword
  (`claims.csv`, `candidate_keywords_zh`) plus embedding search, kept only if they have a transcript and take a position on
  the claim. Target: at least ~300 retrieved items per issue so that ~150 can be hand-labelled; an issue with too few items is
  replaced. **Not built yet** (dataset not downloaded; keyword counts not yet run).
- **Reference reason corpus** — the list of reasons, each tied to a cited source, in `data/reference/` (15 reasons, 8
  sources, 3 claims). It is deliberately **limited, not "balanced"**: it covers only reasons we could source, and the
  claim-endorsing side is thin (1 reason for `strict_only`, 2 for `must_jiwa`, 0 for `bride_price_required`). Reason coverage
  is therefore relative to this list, not to "all views", and the report must say so. `fbx/corpus.py` validates that every
  reason has a side and a source.

## 3. Open items
- Add more sourced claim-endorsing reasons for each issue (e.g. authoritative-parenting literature).
- Re-read S2, S3, S4 from the papers themselves (see `how_checked` in `sources.csv`) before citing in the Final Report.
- Run the keyword counts on ShortVideo and fix issue/claim choice.

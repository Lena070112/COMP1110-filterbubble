# Annotation protocol (v1, 2 Nov 2026)

Applies to every claim in `data/reference/claims.csv`. Unit = one item (video title + ASR transcript). Output = one CSV
per annotator in the format of `data/pilot/annotation_template.csv`. Annotators work **independently** and do not discuss
items until both files are finished.

## 1. Fields
`item_id, t, issue, claim_id, stance, reason, source, status, evidence_passage_or_timestamp`
- `stance`: `strict` / `balanced` / `alt` / `unknown`.
- `reason`: a reason id from `data/reference/reference_reasons.csv` for that claim (e.g. `D3`), or `new:<short text>` if the
  item gives a reason not on the list. Leave blank for `unknown`. If several, use the main one and list others after `;`.
- `source`: the creator/account handle as in the dataset (used only for the source-repetition measure; never published).
- `status`: `ok`, `unknown` (stance undecidable), or `skip` (item is distressing; see section 4).
- `evidence_passage_or_timestamp`: **required** for every `strict`/`balanced`/`alt` label — the sentence from the title or
  transcript that justifies it.

## 2. Stance rules (with examples)
The examples below are **constructed illustrations** (claim `strict_only`), not real videos.

| label | rule | example 1 | example 2 |
|---|---|---|---|
| `strict` | The speaker asserts that strict discipline is the only or necessary way, or dismisses other ways as useless. | 孩子不打不成器，别的方法都没用。 | 管孩子就得严，讲道理没用，只有罚才长记性。 |
| `balanced` | The speaker accepts strictness in part but adds conditions, limits or trade-offs (age, temperament, explaining rules). | 规矩要立，但立完要讲清楚为什么，孩子才会真的接受。 | 严一点没错，但也得看孩子的年龄和性格。 |
| `alt` | The speaker rejects strictness as *the* way, or proposes a different approach as better. | 与其惩罚，不如提前讲好规则，做对了就夸。 | 打骂只会让孩子学会躲和撒谎，没有教会他们对错。 |
| `unknown` | Stance cannot be decided from title + transcript. | A clip of a child crying with music and no speech. | An off-topic clip that only mentions the keyword. |

Decision order: (1) is the item about the issue at all? if not, `unknown`; (2) does the text assert the claim as the only/necessary
route? `strict`; (3) does it reject the claim or promote an alternative? `alt`; (4) otherwise, if it takes a qualified middle
position, `balanced`; (5) if still undecidable, `unknown`. Never guess from tone or from the creator's reputation.

## 3. Special cases
- **Irony and quotation.** Label the *speaker's* stance, not the quoted line. "棍棒底下出孝子——这话害了多少孩子" is `alt`.
- **Several speakers.** Label the stance the item as a whole endorses; if it is a debate with no verdict, `unknown`.
- **Visual-only meaning.** We only see text. If the point is carried by the picture, `unknown`; the unknown share is
  reported, not hidden.
- **Reasons beyond the list.** Use `new:<text>`; new reasons are reviewed jointly and, if they have a citable source, added to
  the reference corpus.
- **Claims that mix issues.** If an item addresses a different claim, use the claim it mainly addresses.

## 4. Welfare and ethics
Some parenting and relationship videos show conflict, violence or distress. Annotators may mark such an item `skip` without
explanation and are never required to finish a batch. Report examples are paraphrased, without creator names. Only title and
transcript text, never viewing histories, go to any LLM API.

## 5. Procedure
1. **Pilot:** both annotators label the same 30 items per issue (development issues first). Compute percent agreement and
   Cohen's kappa with `python scripts/run_annotation_agreement.py A.csv B.csv`.
2. Review every disagreement together (`disagreements` list); record the alternative plausible labels; refine the rules above and
   re-label if a rule was ambiguous. Record the rule change in the file history.
3. If kappa >= 0.6, annotate the reference set (about 150 items per issue each); if not, revise the protocol and repeat the pilot.
4. Held-out issue: annotate only after the protocol is frozen, and do not edit the protocol afterwards.

## 6. Known weaknesses
The reference reason list is small and thin on the claim-endorsing side (see `docs/definitions.md`). Stance labels from titles
and transcripts miss visual content. Two annotators from the same group may share blind spots, which kappa does not reveal.

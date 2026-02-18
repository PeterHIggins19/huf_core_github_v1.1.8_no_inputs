# Contributing to HUF

Thanks for taking a look at the Higgins Unity Framework (HUF)!

HUF is intentionally **small and auditable**: repeatable runs, clear artifacts, and docs that a new reader can follow.
If you can improve clarity, correctness, or reproducibility, that’s a great contribution.

## Quick ways to help

### Report a bug or suggest an improvement
Please open a GitHub Issue and include:
- what you ran (command + OS)
- what you expected vs what happened
- the full error text (or a screenshot)
- if available: the generated `run_stamp.json` and `meta.json`

### Fix docs (high value)
Doc fixes are always welcome: broken links, confusing steps, outdated CLI flags, etc.
Small PRs are easiest to review.

### Code contributions
PRs are welcome, especially for:
- adapter improvements (Planck / Markham / Traffic)
- tests / reproducibility checks
- CLI help text and “quick run” scripts
- performance improvements that keep outputs identical

## Before you open a PR

Please run:
- `python -m pytest -q` (if tests exist in your environment)
- at least one demo case (Traffic or Markham)

If you changed an adapter, include:
- a short before/after note about artifacts (or explain why they changed)

## Style
- Keep changes scoped (one topic per PR)
- Prefer explicit names over clever code
- Add comments where a future reader would ask “why?”

## Contact
If you don’t want to open an Issue, you can email: PeterHiggins@RogueWaveAudio.com

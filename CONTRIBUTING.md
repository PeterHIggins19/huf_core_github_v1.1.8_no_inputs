# Contributing to HUF

Thanks for helping improve HUF. Small, well-scoped contributions are welcome.

## Good contributions
- Docs fixes (especially Windows copy/paste correctness)
- Bug reports with **exact command**, OS, Python version, and `out/*/run_stamp.json`
- Tight PRs that add a small case, improve an adapter, or clarify an artifact

## Style / scope
- Prefer small commits over “big rewrites”
- Keep commands cross-platform (PowerShell + bash)
- If you change behavior, update docs and add a minimal test/fixture when possible

## Testing
Before opening a PR, run at least one end-to-end case and confirm artifacts exist in `out/<case>/`.

## Where to talk
Open an Issue for questions, proposals, or bug reports.

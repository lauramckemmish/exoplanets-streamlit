# Exoplanets Streamlit project guidance

This repository is the Exoplanets Streamlit educational application. This file
defines repository-wide development and deployment behaviour. For
learner-facing work in `experiences/`, follow
[`experiences/AGENTS.md`](experiences/AGENTS.md); use
[`docs/curious_online_style.md`](docs/curious_online_style.md) for
student-facing written voice, and read [`CONTENT_MAP.md`](CONTENT_MAP.md) and
the relevant design document before changing an experience.

Keep stable scientific and data machinery separate from changing pedagogy.
Protect working Experiences and make bounded changes that do not disturb
unrelated learning pathways.

## Development and deployment workflow

This repository currently assumes a single active editor. Routine work happens
directly on `main`, using a bounded change and proportionate verification.

For routine work:

1. Check status/current branch and inspect relevant sources and design documentation.
2. Make the bounded authorised change.
3. Run verification proportionate to the plausible regression risk.
4. Inspect the diff and protect unrelated working functionality.
5. Commit directly to `main`.
6. Push `main`. Never force-push `main`.
7. Perform deployment or live verification only when the change or task warrants it.

Use branches, worktrees, broader testing, synchronization checks, or deployment
verification when the nature or risk of the change warrants them, rather than
as routine process for every small change.

Do not maintain a separate unpublished “better” version that the project owner
cannot inspect unless specifically requested. If tests reveal a serious
regression, credentials or network access prevent a push, or the requested
change risks irreversible loss or corruption of important data, stop and report
the genuine blocker accurately. When network access prevents a push, preserve
the clean committed state and report exactly what remains local rather than
undoing completed work.

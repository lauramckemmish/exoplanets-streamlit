# Exoplanets Streamlit project guidance

This repository is the Exoplanets Streamlit educational application.

Before structural changes, inspect the repository and its existing patterns.
For learner-facing pedagogical work in `experiences/`, follow
[`experiences/AGENTS.md`](experiences/AGENTS.md). For student-facing written
voice, use [`docs/curious_online_style.md`](docs/curious_online_style.md).
Before changing an experience, read [`CONTENT_MAP.md`](CONTENT_MAP.md) and its
relevant design document.

Keep stable scientific and data machinery separate from changing pedagogy.
Protect working Experiences and make bounded changes that do not disturb
unrelated learning pathways.

Current development workflow: inspect → implement → test → inspect diff →
commit → push → merge/update `main` → verify the live Streamlit deployment.
`main` is the working preview environment, so completed bounded changes should
normally be pushed to `main`, not left only locally.

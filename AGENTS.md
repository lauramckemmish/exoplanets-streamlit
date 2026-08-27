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

The deployed Streamlit site is currently the project's working preview
environment.

The project is in active development with a small known audience. Pedagogy,
wording, layout and interaction need to be evaluated in the live deployed
interface. Therefore, unless explicitly instructed otherwise, a completed
bounded implementation should not remain only local or on an unpublished
branch.

For each bounded implementation:

1. Inspect the current repository and relevant design documentation.
2. Make the requested change.
3. Run appropriate tests and checks.
4. Inspect the diff and protect unrelated working functionality.
5. Commit the completed bounded change.
6. Before integration, fetch `origin` and check whether `main` has advanced
   independently. Reconcile legitimate parallel changes safely. Never
   force-push `main` merely to resolve branch divergence.
7. Push the feature/change branch where practical.
8. Merge the completed change into `main`.
9. Push or update `main`.
10. Verify that Streamlit has deployed the latest `main`. Where the deployment
    interface exposes the deployed commit, report its SHA; otherwise report the
    current GitHub `main` SHA and verify that the relevant live experience
    loads successfully.

The live `main` deployment is the primary review artifact for UI and pedagogy
changes.

Do not maintain a separate unpublished “better” version that the project owner
cannot inspect unless specifically requested.

At this stage, rapid visible iteration is more useful than formal
staging/production separation. Git history provides the recovery path if an
iteration needs to be revised or reverted.

If deployment fails after merge, diagnose and repair the deployment rather
than treating a local or unmerged implementation as completion.

Stop before push or merge only if:

- tests reveal a serious regression that cannot safely be resolved;
- credentials, permissions or network access prevent the operation;
- the requested change risks irreversible loss or corruption of important data;
- or the project owner explicitly requests review before merge.

When network access prevents a push, preserve the clean committed state and
report exactly what remains local rather than undoing completed work.

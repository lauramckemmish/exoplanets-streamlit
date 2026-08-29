# Experience authoring

Repository-wide development and deployment rules are defined in the root
[`AGENTS.md`](../AGENTS.md).

Before modifying a student-facing experience implementation in this folder:

1. Read [`docs/curious_online_style.md`](../docs/curious_online_style.md).
2. Read the matching experience `.md` design file (for example, read
   `planet_shopping.md` before editing `planet_shopping.py`).
3. Then inspect and modify the `.py` implementation.

The matching experience design file remains authoritative for that
experience's local pedagogical sequence. Preserve established decisions unless
the user explicitly asks to reconsider them.

## Semantic heading convention

- `st.title()` is the experience or page title.
- `st.header()` introduces a major stage or learning transition.
- `st.subheader()` introduces a genuine subsection within that stage.
- Use ordinary prose for learner instructions and explanations.
- Use the existing learning helpers and components for reasoning prompts,
  reveals, graph-reading support and teacher guidance.
- Use raw Markdown `###` and `####` headings only when they genuinely
  represent that document level, not merely to make text larger.

Visual emphasis should follow the learning or information job. A justified
exception is fine; an unexplained font-size or heading hack is not.

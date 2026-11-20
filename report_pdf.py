"""Build the learner's Planet Shopping report as a PDF (answers, chosen planet and its key facts)."""

from pathlib import Path

from fontTools.ttLib import TTFont
from fpdf import FPDF

FONT_DIR = Path(__file__).resolve().parent / "assets" / "fonts"
_REGULAR = FONT_DIR / "AtkinsonHyperlegible-Regular.ttf"
_BOLD = FONT_DIR / "AtkinsonHyperlegible-Bold.ttf"
_FAMILY = "Atkinson"
_NO_ANSWER = "(not answered)"
_ANSWER_COLOUR = (28, 78, 154)  # the deep blue used for the Data Science circles, so answers stand out


def _printable(text: str, supported: set[int]) -> str:
    """Swap characters the font cannot draw (for example emoji) for '?' so nothing prints as a blank box."""
    cleaned = text.replace("**", "").replace("\r\n", "\n").replace("\r", "\n")
    return "".join(ch if ch == "\n" or ord(ch) in supported else "?" for ch in cleaned)


def build_report_pdf(
    title: str,
    planet_name: str,
    facts: list[tuple[str, str]],
    sections: list[tuple[str, list[tuple[int, str, tuple[str, ...], str]]]],
) -> bytes:
    """Return a PDF.

    ``facts`` is (label, text) pairs for the chosen planet. ``sections`` is (heading, questions), where each
    question is (number, lead-in, follow-up lines, learner's answer).
    """
    supported = set(TTFont(_REGULAR).getBestCmap())

    def clean(text: str) -> str:
        return _printable(text, supported)

    pdf = FPDF(format="A4")
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(True, margin=20)
    pdf.add_font(_FAMILY, "", str(_REGULAR))
    pdf.add_font(_FAMILY, "B", str(_BOLD))
    pdf.set_title(clean(title))
    pdf.add_page()

    def write(
        text: str,
        *,
        bold: bool = False,
        size: float = 11,
        gap: float = 1.5,
        indent: float = 0,
        colour: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        pdf.set_text_color(*colour)
        pdf.set_font(_FAMILY, "B" if bold else "", size)
        pdf.set_x(pdf.l_margin + indent)
        pdf.multi_cell(pdf.epw - indent, size * 0.5 + 1.5, clean(text), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(gap)

    write(title, bold=True, size=20, gap=3)
    write(f"My exoplanet: {planet_name}", bold=True, size=14, gap=2)
    for label, text in facts:
        write(f"{label}: {text}", gap=0.5)
    pdf.ln(4)

    for heading, questions in sections:
        write(heading, bold=True, size=14, gap=2)
        for number, lead_in, follow_ups, answer in questions:
            write(f"{number}. {lead_in}", bold=True, gap=0.5)
            for line in follow_ups:
                write(line, indent=5, gap=0.5)
            write(answer.strip() or _NO_ANSWER, indent=5, gap=3, colour=_ANSWER_COLOUR)
        pdf.ln(3)

    return bytes(pdf.output())

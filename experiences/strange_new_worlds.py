"""Year 8 Strange New Worlds entry point."""

STEP_LABELS = [
    "Welcome", "1 · Meet our Solar System", "2 · Planets around other stars",
    "3 · Discoveries over time", "4 · Compare planet masses", "5 · Strange new worlds",
    "6 · Add orbital distance", "7 · Compare planetary systems", "Conclusion",
]
YEAR_LEVEL = "Year 8"


def render(data, implementation):
    return implementation(data)

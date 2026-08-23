"""CURIOUS facilitator-led exoplanet demographics entry point."""


STEP_LABELS = [
    "Welcome",
    "1 · Our Solar System",
    "2 · Meet exoplanets",
    "3 · Mass and distance",
    "4 · Are we normal?",
    "5 · How we find planets",
    "Conclusion",
]


def render(data, implementation):
    return implementation(data)

"""Introduction catalogue for the available learning experiences."""


def experience_catalog(facilitated_pathway, stage4_pathway, stage5_pathway):
    return [
        (facilitated_pathway, "A fast-paced, facilitator-led CURIOUS experience. Compare planets, change graph scales and discuss why the planets we detect may not tell the whole story."),
        (stage4_pathway, "A two-lesson classroom experience for exploring individual discoveries, growing datasets and the wonderfully varied planetary systems beyond our own."),
        (stage5_pathway, "A two-lesson classroom experience that investigates how different ways of finding planets shape the evidence we have—and the planets we have not yet found."),
        ("Exoplanet Data Laboratory", "An open exploration space for inspecting the NASA dataset, choosing variables, building graphs and testing your own questions."),
        ("Find Your Perfect Planet", "A guided data-science mission: turn a planet idea into testable criteria, inspect candidate worlds and communicate uncertainty in your conclusion."),
    ]

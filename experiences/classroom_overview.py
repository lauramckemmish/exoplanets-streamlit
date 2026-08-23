"""Teacher-facing classroom overview and NSW syllabus alignment content."""

import streamlit as st


NSW_SCIENCE_SYLLABUS_URL = "https://curriculum.nsw.edu.au/learning-areas/science/science-7-10-2023/outcomes"


def render_syllabus_alignment(year_level: str) -> None:
    st.markdown(f"### NSW Science 7–10 Syllabus (2023): {year_level}")
    st.caption(
        "These are direct connections to the current syllabus, implemented from 2026. Teachers should select and "
        "emphasise outcomes to suit their program and students."
    )
    if year_level == "Year 8":
        st.markdown(
            "**Strong content connections**\n\n"
            "- **SC4-OTU-01:** explains how observations are used by scientists to increase knowledge and "
            "understanding of the Universe\n"
            "- **SC4-DA1-01:** explains how data is used by scientists to model and predict scientific phenomena\n\n"
            "**Working Scientifically**\n\n"
            "- **SC4-WS-05:** uses a variety of ways to process and represent data\n"
            "- **SC4-WS-06:** uses data to identify trends, patterns and relationships, and draw conclusions\n"
            "- **SC4-WS-08:** communicates scientific concepts and ideas using a range of communication forms"
        )
    else:
        st.markdown(
            "**Strong content connection**\n\n"
            "- **SC5-DA2-01:** assesses the use of scientific knowledge and data in evidence-based decisions and "
            "when verifying the legitimacy of claims\n\n"
            "**Working Scientifically**\n\n"
            "- **SC5-WS-05:** selects and uses a range of tools to process and represent data\n"
            "- **SC5-WS-06:** analyses data from investigations to identify trends, patterns and relationships, and "
            "draws conclusions\n"
            "- **SC5-WS-08:** communicates scientific arguments with evidence, using scientific language and "
            "terminology in a range of communication forms"
        )
        st.info(
            "**Supporting connection — SC5-WAM-01:** describes the features and applications of different forms of "
            "waves. Transit detection uses measured changes in light, and radial velocity provides an optional "
            "Doppler-effect connection. This activity supports that learning but does not cover the whole outcome."
        )
    st.markdown(f"[View the official NESA outcomes]({NSW_SCIENCE_SYLLABUS_URL})")


def render_classroom_overview(year_level: str, pathway_title: str) -> None:
    st.header(pathway_title)
    st.markdown(
        f"**Teacher positioning:** designed around {('Stage 4 / approximately Year 8' if year_level == 'Year 8' else 'Stage 5 / approximately Year 10')}; adaptable for other cohorts  \n"
        "**Time:** Two lessons of approximately 50 minutes each  \n"
        f"**Learning intention:** {('represent data, identify patterns and communicate a conclusion' if year_level == 'Year 8' else 'analyse data, evaluate how evidence was collected and qualify a claim')}  \n"
        f"**Scientific context:** {('planetary diversity and the growth of exoplanet discoveries' if year_level == 'Year 8' else 'exoplanet detection and the limits of an observed sample')}  \n"
        f"**Evidence of learning:** {('one claim supported by an example or data pattern' if year_level == 'Year 8' else 'a claim supported by evidence and qualified by a limitation')}."
    )
    overview_tab, mapping_tab, syllabus_tab, preparation_tab = st.tabs(
        ["Lesson outline", "Lesson-to-outcome map", "Syllabus outcomes", "Teacher preparation"]
    )
    with overview_tab:
        if year_level == "Year 8":
            st.markdown(
                "**Story:** Start with individual discoveries, build up to counts over time, then use graphs and "
                "case studies to discover that planetary systems can be very different from ours.\n\n"
                "**Lesson 1 — From familiar planets to a growing collection**\n\n"
                "Meet our Solar System, introduce exoplanets through a few memorable examples, look at how the number "
                "of confirmed planets has grown, and compare the mass groups of our planets with detected exoplanets.\n\n"
                "**Lesson 2 — How far away and how strange?**\n\n"
                "Add orbital distance to the mass graph, use linear and log–log representations, and finish with hot "
                "Jupiters and other unusual planetary systems. Detection-method explanations are not part of the Year 8 "
                "student story."
            )
        else:
            st.markdown(
                "**Story:** Use the same NASA data to investigate how measurement methods shape the evidence and the "
                "claims we can make about all planetary systems.\n\n"
                "**Lesson 1 — What do planets look like?**\n\n"
                "Meet Solar System planets and exoplanets, compare their masses, interpret linear and logarithmic "
                "graphs, and consider whether our planetary system is typical.\n\n"
                "**Lesson 2 — How does the way we search shape the data?**\n\n"
                "Investigate direct imaging and transit detection, compare discovery methods, and explain why the "
                "known exoplanets may not represent all planets that exist. Radial velocity/Doppler is available as "
                "an optional supporting connection for teachers using the waves content."
            )
    with mapping_tab:
        if year_level == "Year 8":
            st.markdown(
                "**Lesson 1 — Discovering other worlds**\n\n"
                "- Meet our Solar System: **SC4-WS-05, SC4-WS-08**\n"
                "- Planets around other stars and memorable systems: **SC4-OTU-01**\n"
                "- Annual discoveries: **SC4-OTU-01, SC4-DA1-01, SC4-WS-05, SC4-WS-06**\n"
                "- Compare planet masses: **SC4-WS-05, SC4-WS-06**\n\n"
                "**Lesson 2 — How strange can planetary systems be?**\n\n"
                "- Add orbital distance and compare representations: **SC4-DA1-01, SC4-WS-05, SC4-WS-06**\n"
                "- Strange planets and systems: **SC4-OTU-01, SC4-WS-06**\n"
                "- Final claim plus evidence: **SC4-WS-06, SC4-WS-08**"
            )
        else:
            st.markdown(
                "**Lesson 1 — What does the evidence seem to show?**\n\n"
                "- Meet and compare planets: **SC5-WS-05, SC5-WS-06**\n"
                "- Mass, orbital distance and log–log representation: **SC5-WS-05, SC5-WS-06**\n"
                "- Initial claim about our Solar System: **SC5-DA2-01, SC5-WS-06, SC5-WS-08**\n\n"
                "**Lesson 2 — Can we trust the pattern?**\n\n"
                "- Direct imaging and transit: **SC5-DA2-01, SC5-WS-06**; transit supports **SC5-WAM-01**\n"
                "- Compare methods and revise the claim: **SC5-DA2-01, SC5-WS-06, SC5-WS-08**\n"
                "- Optional radial velocity/Doppler connection: supports **SC5-WAM-01**"
            )
    with syllabus_tab:
        render_syllabus_alignment(year_level)
    with preparation_tab:
        st.markdown(
            "- Allow one internet-connected device per student or pair.\n"
            "- A projector is useful for modelling how to read the first graph.\n"
            "- No specialist software or student login is required.\n"
            "- The default live NASA dataset is cached; a bundled sample is available if the archive is unavailable.\n"
            "- Student responses remain in the current browser session and are not submitted to the teacher.\n"
            "- Lesson 1 has a clearly marked stopping point after Step 4."
        )

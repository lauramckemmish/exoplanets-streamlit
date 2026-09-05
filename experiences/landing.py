"""Introduction page for the exoplanet learning experiences."""

from datetime import date
from pathlib import Path

import streamlit as st

from visual_system import resource_identity, semantic_heading


def _render_cards(entries, *, button_label, button_key_prefix, open_item):
    """Render a compact two-column collection of landing-page destinations."""
    def render_card(entry):
        with st.container(border=True):
            thumbnail = entry.get("thumbnail")
            if thumbnail:
                semantic_heading(entry["name"], "subsection")
                st.write(entry["summary"])
                st.markdown(
                    "<style>"
                    ".st-key-planet-shopping-thumbnail { max-width: 30rem; width: 100%; margin: 0 auto; }"
                    "</style>",
                    unsafe_allow_html=True,
                )
                with st.container(key="planet-shopping-thumbnail"):
                    st.image(Path(__file__).resolve().parent.parent / thumbnail, use_container_width=True)
                st.button(
                    button_label,
                    key=f"{button_key_prefix}_{entry['name']}",
                    on_click=open_item,
                    args=(entry["name"],),
                )
                return
            semantic_heading(f"{entry['icon']} {entry['name']}", "subsection")
            st.write(entry["summary"])
            st.button(
                button_label,
                key=f"{button_key_prefix}_{entry['name']}",
                use_container_width=True,
                on_click=open_item,
                args=(entry["name"],),
            )

    for left, right in zip(entries[::2], entries[1::2]):
        first, second = st.columns(2)
        for column, entry in zip((first, second), (left, right)):
            with column:
                render_card(entry)
    if len(entries) % 2:
        _, card_column, _ = st.columns([1, 2, 1])
        with card_column:
            render_card(entries[-1])


def render(data, image_path, portrait_logo_path, feedback_url, grant_url, catalog, open_experience, open_explore_resource, source):
    st.title("Other worlds are becoming data")
    introduction_column, image_column = st.columns([3, 2])
    with introduction_column:
        st.markdown(
            "For most of human history, we knew about one planetary system: our own. "
            "That has changed."
        )
        st.markdown(
            "We now know thousands of planets orbiting other stars, and the catalogue is "
            "still growing. New planets are being discovered, old observations are being "
            "analysed in new ways, and new telescopes are opening questions that could not "
            "previously be asked."
        )
        if source.is_live:
            current_date = date.today()
            date_label = f"{current_date.day} {current_date.strftime('%b %Y')}"
            st.metric(
                f"Live count of confirmed exoplanets in the NASA archive · {date_label}",
                f"{len(data):,}",
            )
        else:
            st.metric("Bundled NASA-derived catalogue sample", f"{len(data):,}")
            st.caption("Live archive unavailable — using the bundled sample.")
    with image_column:
        st.image(
            image_path,
            caption="Artist's concept of the variety of known exoplanets. Credit: NASA/JPL-Caltech",
            use_container_width=True,
        )
    semantic_heading("Choose an investigation", "major-section")
    st.write("Follow a guided investigation designed for a classroom or workshop.")
    experiences = catalog.experience_catalog()
    _render_cards(
        experiences,
        button_label="Open experience →",
        button_key_prefix="open_experience",
        open_item=open_experience,
    )
    semantic_heading("Explore the data", "major-section")
    st.write("Follow a question or dataset that interests you.")
    _render_cards(
        catalog.explore_catalog(),
        button_label="Explore resource →",
        button_key_prefix="open_explore",
        open_item=open_explore_resource,
    )
    st.divider()
    with st.container(width=1080):
        with st.container(key="landing_about_label"):
            st.markdown("About this resource")
        resource_identity(
            "Data Science with Planets Beyond Our Solar System",
            portrait_logo_path,
            logo_width=125,
        )
        with st.container(key="landing_stewardship", border=True):
            st.markdown(
                "**Resource stewardship and scientific review · Dr Laura McKemmish, UNSW Chemistry**  \n"
                "*Computational astrochemist · 10+ years creating research-connected science experiences and data-rich investigations for school students*"
            )
        st.write(
            "Interactive learning experiences and an open data lab for investigating real data from the NASA "
            "Exoplanet Archive.\n\n"
            "Developed at UNSW through CURIOUS, a regional science outreach program connecting school students "
            "with university science."
        )
        with st.expander("Why we developed this resource"):
            st.write(
                "Planets Beyond grows from more than a decade of developing research-connected science "
                "experiences and computational learning for school and university students.\n\n"
                "At UNSW, this work has included large-scale school research programs, university teaching "
                "in Python and computational science, and professional development helping science teachers "
                "prepare for data science in the school curriculum. Teacher data-science work was supported "
                "by Google and philanthropic funding.\n\n"
                "Across these settings, the same challenge kept appearing: the important skill is not simply "
                "learning to code. It is learning how to ask questions of data, make evidence-based choices, "
                "recognise uncertainty and decide what the evidence supports.\n\n"
                "Planets Beyond brings that experience into accessible investigations using real exoplanet data."
            )
            st.markdown(
                "**Built from experience across:** School research experiences · Teacher professional "
                "learning · University data-science teaching · Scientific research"
            )
        with st.expander("Development, feedback and acknowledgements"):
            semantic_heading("Development and feedback", "subsection")
            st.info("**Currently in development**\n\nThis resource is being actively developed. Please expect some content and features to change while it is refined.")
            if feedback_url:
                st.link_button("Give teacher feedback", feedback_url)
            st.markdown(
                "Feedback is very welcome—especially detailed suggestions from teachers and "
                "facilitators. Please email [l.mckemmish@unsw.edu.au](mailto:l.mckemmish@unsw.edu.au)."
            )
            semantic_heading("People and perspectives behind this resource", "subsection")
            st.markdown(
                "Planets Beyond has been shaped by people bringing different kinds of expertise and experience. "
                "These credits recognise the perspectives and intellectual contributions that have influenced "
                "the resource and the approach behind it."
            )
            st.markdown(
                "**Isabella Bustos-McNeil** — *near-peer perspective*\n\n"
                "**James Cleaver** — *data-science perspective*\n\n"
                "**Laura McKemmish** — *research translation · pedagogical expertise*\n\n"
                "**Lauren McKnight** — *pedagogical expertise*\n\n"
                "**Maria Pettyjohn** — *research translation*\n\n"
                "**Charlotte Regan** — *teacher perspective*\n\n"
                "**Laura Smith** — *teacher perspective*\n\n"
                "**Anna-Maree Syme** — *research translation*\n\n"
                "**Juan Camilo Zapata Trujillo** — *research translation*"
            )
            st.markdown(
                "We also acknowledge the facilitators, teachers and students whose observations and feedback "
                "continue to inform the resource."
            )
            semantic_heading("Support and partnerships", "subsection")
            st.markdown(
                f"[Australian Government Maker Projects – Community STEM Engagement Grant]({grant_url})\n\n"
                "This work has been developed with contributions from CSIRO through the "
                "STEM-INSIGHTS program and the UNSW Student Equity Team."
            )

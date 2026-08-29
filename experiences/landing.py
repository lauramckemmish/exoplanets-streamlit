"""Introduction page for the exoplanet learning experiences."""

from pathlib import Path

import streamlit as st

from ui_helpers import logo_plate


def _render_cards(entries, *, button_label, button_key_prefix, open_item):
    """Render a compact two-column collection of landing-page destinations."""
    def render_card(entry):
        with st.container(border=True):
            thumbnail = entry.get("thumbnail")
            if thumbnail:
                st.markdown(f"### {entry['name']}")
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
            st.markdown(f"### {entry['icon']} {entry['name']}")
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
            st.metric("Confirmed exoplanets in the NASA archive", f"{len(data):,}")
            st.caption("**Live NASA catalogue** · count changes as new planets are confirmed")
        else:
            st.metric("Planets in the bundled notebook sample", f"{len(data):,}")
            st.caption("This bundled sample supports offline use. Its row count is not the current confirmed-planet total.")
    with image_column:
        st.image(
            image_path,
            caption="Artist's concept of the variety of known exoplanets. Credit: NASA/JPL-Caltech",
            use_container_width=True,
        )
    st.markdown("## Experience something")
    st.write("Follow a guided investigation. These experiences carry a question, story or dataset through a classroom or workshop sequence.")
    experiences = catalog.experience_catalog()
    _render_cards(
        experiences,
        button_label="Open experience →",
        button_key_prefix="open_experience",
        open_item=open_experience,
    )
    st.markdown("## Explore something")
    st.write("Follow a question, story or dataset that interests you.")
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
        logo_column, stewardship_column = st.columns([0.5, 4.5], gap="small")
        with logo_column:
            logo_plate(portrait_logo_path, width=60, alt="UNSW Sydney")
        with stewardship_column:
            st.markdown("### Data Science with Planets Beyond Our Solar System")
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
        with st.expander("Program history"):
            st.markdown("### Earlier development")
            st.write(
                "This work builds on earlier UNSW work supporting teachers and students to use "
                "data science in school science, helping establish reusable learning resources "
                "and approaches."
            )
            st.markdown("### CURIOUS regional program")
            st.write(
                "CURIOUS extended this work through research-connected STEM workshops with "
                "regional schools in 2025–26. The program was enabled by a $100,000 Australian "
                "Government Maker Projects – Community STEM Engagement Grant and a partnership "
                "with Passionately Curious."
            )
            st.write(
                "These online resources are part of CURIOUS's continuing development: capturing "
                "what is learned through real delivery and turning it into reusable resources for "
                "students, teachers and facilitators."
            )
        with st.expander("Development, feedback and acknowledgements"):
            st.info("**Currently in development**\n\nThis resource is being actively developed. Please expect some content and features to change while it is refined.")
            if feedback_url:
                st.link_button("Give teacher feedback", feedback_url)
            st.markdown(
                "Feedback is very welcome—especially detailed suggestions from teachers and "
                "facilitators. Please email [l.mckemmish@unsw.edu.au](mailto:l.mckemmish@unsw.edu.au)."
            )
            st.markdown(
                f"### Funding\n\n"
                f"[Australian Government Maker Projects – Community STEM Engagement Grant]({grant_url})"
            )
            st.markdown(
                "### Partners\n\n"
                "This work has been developed with contributions from CSIRO through the "
                "STEM-INSIGHTS program and the UNSW Student Equity Team."
            )
            st.markdown(
                "### Contributors to this resource\n\n"
                "- Isabella Bustos-McNeil\n"
                "- James Cleaver\n"
                "- Laura McKemmish\n"
                "- Lauren McKnight\n"
                "- Maria Pettyjohn\n"
                "- Charlotte Regan\n"
                "- Laura Smith\n\n"
                "We also gratefully acknowledge the CURIOUS facilitators, teachers and students "
                "whose ideas, observations, feedback and experience have helped test and improve "
                "this resource."
            )

"""Introduction page for the exoplanet learning experiences."""

import streamlit as st


def _render_cards(entries, *, button_label, button_key_prefix, open_item):
    """Render a compact two-column collection of landing-page destinations."""
    for left, right in zip(entries[::2], entries[1::2]):
        first, second = st.columns(2)
        for column, entry in zip((first, second), (left, right)):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {entry['icon']} {entry['name']}")
                    st.write(entry["summary"])
                    st.button(
                        button_label,
                        key=f"{button_key_prefix}_{entry['name']}",
                        use_container_width=True,
                        on_click=open_item,
                        args=(entry["name"],),
                    )
    if len(entries) % 2:
        with st.container(border=True):
            entry = entries[-1]
            st.markdown(f"### {entry['icon']} {entry['name']}")
            st.write(entry["summary"])
            st.button(
                button_label,
                key=f"{button_key_prefix}_{entry['name']}",
                use_container_width=True,
                on_click=open_item,
                args=(entry["name"],),
            )


def render(data, image_path, feedback_url, grant_url, catalog, open_experience, open_explore_resource):
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
        st.metric("Confirmed exoplanets in the NASA archive", f"{len(data):,}")
        st.caption("This is live catalogue evidence, not a fixed fact. Come back later and that number may be different.")
    with image_column:
        st.image(
            image_path,
            caption="Artist's concept of the variety of known exoplanets. Credit: NASA/JPL-Caltech",
            use_container_width=True,
        )

    st.markdown("## Why I made this")
    st.markdown(
        "I’m Dr Laura McKemmish, a UNSW scientist working with molecules, spectroscopy "
        "and exoplanet science. I’ve been able to watch this field change while working in it."
    )
    st.markdown(
        "One of the things I love about this science is that you don’t have to wait until "
        "you are a professional astronomer to start asking real questions. The tools and "
        "depth change, but the important moves are recognisable: look at the evidence, "
        "understand how it was measured, notice what is surprising, and ask what the data "
        "can and cannot tell us. Come and investigate this with me."
    )
    with st.expander("Laura’s exoplanet story"):
        st.write(
            "I first became involved in exoplanet research in 2014. Since then, I’ve watched "
            "the catalogue and the questions astronomers can ask change quickly. I’ve explored "
            "related questions with high-school and university students, and with PhD researchers."
        )

    st.markdown("## Experiences")
    st.write("Follow a guided investigation. These experiences carry a question, story or dataset through a classroom or workshop sequence.")
    experiences = catalog.experience_catalog()
    _render_cards(
        experiences,
        button_label="Open experience →",
        button_key_prefix="open_experience",
        open_item=open_experience,
    )
    st.markdown("## Explore")
    st.write("Follow a question, story or dataset that interests you.")
    _render_cards(
        catalog.explore_catalog(),
        button_label="Explore resource →",
        button_key_prefix="open_explore",
        open_item=open_explore_resource,
    )
    with st.expander("Development, feedback and acknowledgements"):
        st.info("**Currently in development**\n\nThis resource is being actively developed. Please expect some content and features to change while it is refined.")
        if feedback_url:
            st.link_button("Give teacher feedback", feedback_url)
        st.markdown(f"Feedback is very welcome—especially detailed suggestions from teachers and facilitators. Please email [l.mckemmish@unsw.edu.au](mailto:l.mckemmish@unsw.edu.au).\n\n**Developed for UNSW CURIOUS**\n\nCreated by **Maria Pettyjohn, Dr Lauren McKnight, James Cleaver and Dr Laura McKemmish**.\n\nThis resource has also been shaped by the ideas, observations and feedback of many CURIOUS facilitators, teachers and student participants. We gratefully acknowledge everyone who has helped test and improve it over time.\n\nDevelopment was supported through the Australian Government's [Maker Projects: Community STEM Engagement Grants 2024 program]({grant_url}).")

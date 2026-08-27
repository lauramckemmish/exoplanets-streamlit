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
    st.title("Explore exoplanets using real NASA data")
    count_column, description_column, image_column = st.columns([1, 2, 2])
    with count_column:
        st.metric("Confirmed exoplanets", f"{len(data):,}")
    with description_column:
        st.markdown("Astronomers have confirmed thousands of planets orbiting stars beyond our Sun. This number comes from the NASA Exoplanet Archive and grows as new observations are analysed.")
    with image_column:
        st.image(image_path, caption="Artist's concept of the variety of known exoplanets. Credit: NASA/JPL-Caltech", use_container_width=True)
    st.markdown("**Developed for UNSW CURIOUS**")
    st.info("**Currently in development**\n\nThis resource is being actively developed. Please expect some content and features to change during this period; a stable version will be created in due course.\n\nFeedback is very welcome—especially detailed suggestions from teachers and facilitators. The resource is easy to update, so content can readily be added, removed or revised. Please email [l.mckemmish@unsw.edu.au](mailto:l.mckemmish@unsw.edu.au), and feel free to share the resource with colleagues and through your local networks.")
    if feedback_url:
        st.link_button("Give teacher feedback", feedback_url, type="primary")
    st.markdown("## Experiences")
    st.write("Guided investigations for classrooms and workshops.")
    experiences = catalog.experience_catalog()
    _render_cards(
        experiences,
        button_label="Open experience →",
        button_key_prefix="open_experience",
        open_item=open_experience,
    )
    st.markdown("## Explore")
    st.write("Dig deeper into the science, data and stories.")
    _render_cards(
        catalog.explore_catalog(),
        button_label="Explore resource →",
        button_key_prefix="open_explore",
        open_item=open_explore_resource,
    )
    with st.expander("About and acknowledgements"):
        st.markdown(f"**Developed for UNSW CURIOUS**\n\nCreated by **Maria Pettyjohn, Dr Lauren McKnight, James Cleaver and Dr Laura McKemmish**.\n\nThis resource has also been shaped by the ideas, observations and feedback of many CURIOUS facilitators, teachers and student participants. We gratefully acknowledge everyone who has helped test and improve it over time.\n\nDevelopment was supported through the Australian Government's [Maker Projects: Community STEM Engagement Grants 2024 program]({grant_url}).\n\n**Contact:** Dr Laura McKemmish — [l.mckemmish@unsw.edu.au](mailto:l.mckemmish@unsw.edu.au)")

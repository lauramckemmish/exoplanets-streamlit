"""Introduction page for the exoplanet learning experiences."""

import streamlit as st


def render(data, image_path, feedback_url, grant_url, catalog, facilitated_pathway, stage4_pathway, stage5_pathway, open_experience):
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
    st.markdown("## Choose an experience\nUse the sidebar to open the experience that suits your group.")
    experiences = catalog.experience_catalog(facilitated_pathway, stage4_pathway, stage5_pathway)
    for left, right in zip(experiences[::2], experiences[1::2]):
        first, second = st.columns(2)
        for column, (name, summary) in zip((first, second), (left, right)):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {name}")
                    st.write(summary)
                    st.button("Open experience →", key=f"open_experience_{name}", use_container_width=True, on_click=open_experience, args=(name, facilitated_pathway, stage4_pathway, stage5_pathway))
    if len(experiences) % 2:
        with st.container(border=True):
            st.markdown(f"### {experiences[-1][0]}")
            st.write(experiences[-1][1])
            st.button("Open experience →", key=f"open_experience_{experiences[-1][0]}", use_container_width=True, on_click=open_experience, args=(experiences[-1][0], facilitated_pathway, stage4_pathway, stage5_pathway))
    with st.expander("About and acknowledgements"):
        st.markdown(f"**Developed for UNSW CURIOUS**\n\nCreated by **Maria Pettyjohn, Dr Lauren McKnight, James Cleaver and Dr Laura McKemmish**.\n\nThis resource has also been shaped by the ideas, observations and feedback of many CURIOUS facilitators, teachers and student participants. We gratefully acknowledge everyone who has helped test and improve it over time.\n\nDevelopment was supported through the Australian Government's [Maker Projects: Community STEM Engagement Grants 2024 program]({grant_url}).\n\n**Contact:** Dr Laura McKemmish — [l.mckemmish@unsw.edu.au](mailto:l.mckemmish@unsw.edu.au)")

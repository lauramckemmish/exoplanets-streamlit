"""Exoplanet Data Laboratory experience entry point."""

import pandas as pd
import plotly.express as px
import streamlit as st

TITLE = "Exoplanet Data Laboratory"
SUBTITLE = "Open exploration with contextual guidance for analytical choices"
TAB_LABELS = [
    "Start here",
    "Variables",
    "Dataset and missing values",
    "One variable",
    "Two variables",
    "Three variables",
    "Sky map",
]

TEACHER_GUIDANCE = {
    "title": "Exoplanet Data Laboratory",
    "purpose": "Support open-ended exploration while making analytical choices visible and discussable.",
    "approach": "Invite students to state a question before changing variables. Ask what each axis, colour and scale contributes, and whether missing data or detection methods could affect the pattern.",
    "alignment": "NSW Science 7–10 Working Scientifically: process and analyse secondary data; construct and use representations; identify trends, patterns and relationships; draw evidence-based conclusions; evaluate data quality and limitations.",
    "timing": "Flexible investigation",
    "listen_for": "Students explaining why a graph answers a particular question rather than treating graph settings as decoration.",
}

SYLLABUS_LANGUAGE = {
    "stage4": "Stage 4 emphasis: summarise data from secondary sources; use tables and graphs; identify trends, patterns and relationships; use evidence to support or discount a question; and reflect on data quality.",
    "stage5": "Stage 5 extension: explain relationships between variables, evaluate reliability and limitations, and assess how the source and collection of data affect a claim.",
}

DATASET_FIELDS = [
    ("Planet name", "pl_name"),
    ("Host star", "hostname"),
    ("Discovery year", "disc_year"),
    ("Discovery method", "discoverymethod"),
    ("Planet radius (Earth radii)", "pl_rade"),
    ("Planet mass (Earth masses)", "pl_bmasse"),
    ("Orbital period (days)", "pl_orbper"),
    ("Equilibrium temperature (K)", "pl_eqt"),
    ("Distance from Earth (light-years)", "sy_dist"),
    ("Known stars in system", "sy_snum"),
    ("Known planets in system", "sy_pnum"),
]

PHYSICAL_GROUPS = {
    "Planet mass (Earth masses)": ("pl_bmasse", [-float("inf"), 1, 10, 100, 1000, float("inf")], ["Less than 1 Earth mass", "1–10 Earth masses", "10–100 Earth masses", "100–1,000 Earth masses", "More than 1,000 Earth masses"]),
    "Planet radius (Earth radii)": ("pl_rade", [-float("inf"), 1, 2, 4, 10, float("inf")], ["Less than 1 Earth radius", "1–2 Earth radii", "2–4 Earth radii", "4–10 Earth radii", "More than 10 Earth radii"]),
    "Equilibrium temperature (K)": ("pl_eqt", [-float("inf"), 200, 300, 500, 1000, float("inf")], ["Below 200 K", "200–300 K", "300–500 K", "500–1,000 K", "Above 1,000 K"]),
    "Orbital period": ("pl_orbper", [-float("inf"), 1, 7, 30, 365, 3650, float("inf")], ["Less than 1 day", "1–7 days", "7–30 days", "30 days–1 year", "1–10 years", "More than 10 years"]),
    "Orbital distance (AU)": ("pl_orbsmax", [-float("inf"), 0.1, 1, 5, 30, float("inf")], ["Less than 0.1 AU", "0.1–1 AU", "1–5 AU", "5–30 AU", "More than 30 AU"]),
}


def render_intro(data, guidance_mode, guidance_box):
    st.header("What is the Exoplanet Data Laboratory?")
    guidance_box(guidance_mode, "Use real NASA data to ask questions, choose variables and build graphs about planets beyond our Solar System.", "Frame this as open investigation: students make analytical choices, inspect patterns and discuss what the data can and cannot show.")
    st.subheader("First: what is an exoplanet?")
    st.write("An exoplanet is a planet orbiting a star other than our Sun. The Milky Way probably contains about 400 billion stars, and most stars are thought to have planets. That means there may be an enormous number of planets in our galaxy.")
    st.subheader("How does a planet become a data record?")
    st.write("Astronomers usually cannot see an exoplanet directly. They measure clues from its star—for example, a tiny dip in starlight when a planet crosses in front of the star (a transit), or a small change in the star's motion caused by the planet's gravity (radial velocity). Repeated measurements can be analysed to estimate properties such as planet size, mass and orbital distance.")
    st.subheader("What are we looking at here?")
    st.write("Each row represents one known exoplanet record. This is an incomplete sample: it contains planets that have been detected and confirmed, not every planet that exists. Many known systems are hundreds to a few thousand light-years away, and most of the Milky Way has not been searched in the same way.")
    st.caption("Sources: [NASA — What is an exoplanet?](https://science.nasa.gov/exoplanets/what-is-an-exoplanet/) · [NASA — Kepler's legacy](https://science.nasa.gov/exoplanets/keplerscience/)")
    st.info("A graph is an answer to a question. Before changing a setting, say what you want to find out.")
    st.subheader("A useful investigation cycle")
    st.markdown("1. Ask a question  \n2. Choose variables  \n3. Make a graph  \n4. Describe the pattern  \n5. Consider what might affect the pattern")
    if guidance_mode == "Teacher":
        with st.expander("NSW syllabus connections", expanded=False):
            st.write(SYLLABUS_LANGUAGE["stage4"])
            st.write(SYLLABUS_LANGUAGE["stage5"])


def render_summary(data, guidance_mode):
    st.header("A quick summary of the data")
    st.write("These numbers describe the records in this table. They do not describe every planet that exists.")
    a, b, c = st.columns(3)
    a.metric("Planet records", f"{len(data):,}")
    b.metric("Host stars", f"{data['hostname'].nunique():,}")
    c.metric("Discovery methods", f"{data['discoverymethod'].nunique():,}")
    if guidance_mode != "Minimal":
        st.caption("The number of records can change as astronomers confirm new planets and update the archive.")


def display_data(data):
    """Return a copy with student-facing distance values shown in light-years."""
    shown = data.copy()
    shown["sy_dist"] = shown["sy_dist"] * 3.26156
    return shown


def render_variables(data, guidance_mode, field_options, variables, variable_card, scale_guidance):
    st.header("Variables")
    st.write("A variable is a feature we can record or compare. The archive field is the short name used in the NASA table.")
    variable_rows = [{"Variable": label, "NASA archive field": field, "What it tells us": variables.get(field, {}).get("description", "")} for label, field in DATASET_FIELDS]
    st.dataframe(pd.DataFrame(variable_rows), use_container_width=True, hide_index=True)
    selected_label = st.selectbox("Choose a variable to explore", list(field_options), key="dictionary_variable")
    variable_card(data, field_options[selected_label], guidance_mode, variables, scale_guidance)


def render_dataset_table(data):
    st.header("Dataset")
    st.write("Each row is one known exoplanet record. This is a sample of what astronomers have measured so far—not a list of every planet that exists.")
    display = [field for _, field in DATASET_FIELDS]
    friendly_columns = {field: label for label, field in DATASET_FIELDS}
    st.dataframe(display_data(data)[display].rename(columns=friendly_columns), use_container_width=True, hide_index=True)


def render_missing(data, guidance_mode):
    st.header("Missing data")
    st.write("A blank value means that property has not been recorded for that planet. It does not mean zero or that the property does not exist.")
    display = [field for _, field in DATASET_FIELDS]
    missing = pd.DataFrame({"Variable": [label for label, _ in DATASET_FIELDS], "Missing records": [int(data[col].isna().sum()) for col in display], "Complete records (%)": [round(100 * data[col].notna().mean(), 1) for col in display]}).sort_values("Complete records (%)")
    st.dataframe(missing, use_container_width=True, hide_index=True)
    if guidance_mode != "Minimal":
        st.info("Missing values limit which questions can be answered reliably.")


def render_dataset_and_missing(data, guidance_mode):
    """Show the data table, basic counts and recorded-value limitations together."""
    st.header("Dataset and missing values")
    st.write("Each row is one known exoplanet record. This table is a sample of what astronomers have measured so far—not a list of every planet that exists.")
    a, b, c = st.columns(3)
    a.metric("Planet records", f"{len(data):,}")
    b.metric("Host stars", f"{data['hostname'].nunique():,}")
    c.metric("Discovery methods", f"{data['discoverymethod'].nunique():,}")
    display = [field for _, field in DATASET_FIELDS]
    friendly_columns = {field: label for label, field in DATASET_FIELDS}
    st.dataframe(display_data(data)[display].rename(columns=friendly_columns), use_container_width=True, hide_index=True)
    st.subheader("What does a blank value mean?")
    st.write("A blank value means that property has not been recorded for that planet. It does not mean zero or that the property does not exist.")
    missing = pd.DataFrame({"Variable": [label for label, _ in DATASET_FIELDS], "Missing records": [int(data[col].isna().sum()) for col in display], "Complete records (%)": [round(100 * data[col].notna().mean(), 1) for col in display]}).sort_values("Complete records (%)")
    st.dataframe(missing, use_container_width=True, hide_index=True)
    if guidance_mode == "Teacher":
        st.caption("NSW Science link: process and analyse secondary data, including evaluating the quality and limitations of data.")


def numeric_options(field_options):
    return {label: field for label, field in field_options.items() if field != "discoverymethod"}


def render_one_variable(data, guidance_mode, field_options):
    st.header("One variable")
    st.write("Start by looking at one variable. A histogram counts how many records fall into each range; for an existing category, the same idea appears as a bar-count graph.")

    st.subheader("A. Start with a histogram")
    histogram_choices = {**numeric_options(field_options), "Discovery method": "discoverymethod"}
    histogram_label = st.selectbox("Choose a variable", list(histogram_choices), key="lab_one_histogram")
    histogram_field = histogram_choices[histogram_label]
    histogram_data = display_data(data) if histogram_field == "sy_dist" else data
    if histogram_field == "discoverymethod":
        figure = px.histogram(histogram_data.dropna(subset=[histogram_field]), x=histogram_field, title=f"Counts by {histogram_label}")
        figure.update_layout(xaxis_title=histogram_label, yaxis_title="Number of planet records")
        st.caption("For a category such as discovery method, the histogram is read like a bar chart: one bar for each group.")
    else:
        bin_count = st.slider("Number of histogram ranges", min_value=5, max_value=60, value=20, help="The histogram groups nearby values into ranges. More ranges show finer detail; fewer ranges show a simpler overall pattern.")
        figure = px.histogram(histogram_data.dropna(subset=[histogram_field]), x=histogram_field, nbins=bin_count, title=f"Histogram of {histogram_label}")
        figure.update_layout(xaxis_title=histogram_label, yaxis_title="Number of planet records")
    st.plotly_chart(figure, use_container_width=True)

    st.subheader("B. Group values using planet and Solar System analogies")
    st.write("Sometimes equal-width histogram ranges are not the most meaningful groups. Scientists can also use ranges linked to familiar planets and orbital scales.")
    group_label = st.selectbox("Choose a measurement to group", list(PHYSICAL_GROUPS), key="lab_one_physical_group")
    group_field, breaks, labels = PHYSICAL_GROUPS[group_label]
    group_values = data[group_field].dropna()
    groups = pd.cut(group_values, bins=breaks, labels=labels, include_lowest=True)
    group_counts = groups.value_counts(sort=False).reset_index()
    group_counts.columns = ["Group", "Number of planet records"]
    group_chart = st.radio("Show these groups as", ["Bar chart", "Pie chart"], horizontal=True, key="lab_one_group_chart")
    if group_chart == "Bar chart":
        grouped_figure = px.bar(group_counts, x="Group", y="Number of planet records", title=f"{group_label}, grouped into meaningful ranges")
        grouped_figure.update_layout(xaxis_tickangle=-35)
    else:
        grouped_figure = px.pie(group_counts, names="Group", values="Number of planet records", title=f"{group_label}, grouped into meaningful ranges")
    st.plotly_chart(grouped_figure, use_container_width=True)
    if guidance_mode != "Minimal":
        st.info("Compare the histogram ranges with the physical groups. What story does each representation make easier to tell? NSW Science link: organise and summarise secondary data using an appropriate representation.")


def render_two_variables(data, guidance_mode, field_options):
    st.header("Two variables")
    st.write("Choose two variables and look for a pattern. They might both be measurements, or one might describe a group.")
    options = numeric_options(field_options)
    all_options = {**options, "Discovery method": "discoverymethod"}
    left, right = st.columns(2)
    x_label = left.selectbox("Horizontal variable", list(all_options), index=list(all_options.values()).index("pl_orbsmax"), key="lab_two_x")
    y_label = right.selectbox("Vertical variable", list(all_options), index=list(all_options.values()).index("pl_bmasse"), key="lab_two_y")
    x_field, y_field = all_options[x_label], all_options[y_label]
    plotted = display_data(data) if "sy_dist" in {x_field, y_field} else data
    scale_left, scale_right = st.columns(2)
    use_log_x = scale_left.checkbox("Use a logarithmic horizontal axis", disabled=x_field == "discoverymethod", key="lab_two_log_x")
    use_log_y = scale_right.checkbox("Use a logarithmic vertical axis", disabled=y_field == "discoverymethod", key="lab_two_log_y")
    valid = plotted.dropna(subset=[x_field, y_field])
    if use_log_x:
        valid = valid[valid[x_field] > 0]
    if use_log_y:
        valid = valid[valid[y_field] > 0]
    figure = px.scatter(valid, x=x_field, y=y_field, hover_name="pl_name", title=f"{y_label} and {x_label}")
    figure.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    if use_log_x:
        figure.update_xaxes(type="log")
    if use_log_y:
        figure.update_yaxes(type="log")
    st.plotly_chart(figure, use_container_width=True)
    if guidance_mode != "Minimal":
        st.info("Describe the pattern first. Then try a log axis if small and large values are crowded together. The values stay the same; only the spacing changes. NSW Science link: identify trends, patterns and relationships in secondary data.")


def render_three_variables(data, guidance_mode, field_options):
    st.header("Three variables")
    st.write("Choose a horizontal variable, a vertical variable and a colour variable. Colour can show an existing category, a numerical scale or one of the meaningful groups used in One Variable.")
    options = numeric_options(field_options)
    all_options = {**options, "Discovery method": "discoverymethod"}
    left, middle, right = st.columns(3)
    x_label = left.selectbox("Horizontal variable", list(all_options), index=list(all_options.values()).index("pl_orbsmax"), key="lab_three_x")
    y_label = middle.selectbox("Vertical variable", list(all_options), index=list(all_options.values()).index("pl_bmasse"), key="lab_three_y")
    colour_options = ["Discovery method", "Discovery year"] + [f"{label} group" for label in PHYSICAL_GROUPS]
    category_label = right.selectbox("Colour variable", colour_options, key="lab_three_category")
    x_field, y_field = all_options[x_label], all_options[y_label]
    plotted = display_data(data) if "sy_dist" in {x_field, y_field} else data
    if category_label.endswith(" group"):
        group_label = category_label.removesuffix(" group")
        group_field, breaks, labels = PHYSICAL_GROUPS[group_label]
        plotted = plotted.copy()
        colour_field = "_colour_group"
        plotted[colour_field] = pd.cut(plotted[group_field], bins=breaks, labels=labels, include_lowest=True)
    else:
        colour_field = "discoverymethod" if category_label == "Discovery method" else "disc_year"
    scale_left, scale_right = st.columns(2)
    use_log_x = scale_left.checkbox("Use a logarithmic horizontal axis", disabled=x_field == "discoverymethod", key="lab_three_log_x")
    use_log_y = scale_right.checkbox("Use a logarithmic vertical axis", disabled=y_field == "discoverymethod", key="lab_three_log_y")
    valid = plotted.dropna(subset=[x_field, y_field, colour_field])
    if use_log_x:
        valid = valid[valid[x_field] > 0]
    if use_log_y:
        valid = valid[valid[y_field] > 0]
    figure = px.scatter(valid, x=x_field, y=y_field, color=colour_field, hover_name="pl_name", title=f"{y_label} and {x_label}, coloured by {category_label}")
    figure.update_layout(xaxis_title=x_label, yaxis_title=y_label, legend_title=category_label)
    if use_log_x:
        figure.update_xaxes(type="log")
    if use_log_y:
        figure.update_yaxes(type="log")
    st.plotly_chart(figure, use_container_width=True)
    if guidance_mode != "Minimal":
        st.info("Ask whether the coloured groups occupy different parts of the graph. Try log axes if small and large values are crowded together, then consider whether the way the data were collected could affect the pattern. NSW Science link: use representations to analyse evidence and evaluate data limitations.")

DISCOVERY_GUIDANCE = {
    "summary": "Use this graph to compare categories over time. Look for changes in dominant discovery methods, sudden increases and periods with sparse data.",
    "teacher": "Ask whether the graph describes the true planet population or the history of available detection methods and surveys.",
    "prompt": "**Look for:** changes over time, dominant categories and sudden shifts.  \n**Consider:** whether detection methods favour certain types of planets.  \n**Describe:** 'Discoveries using ______ increased after ______, which may reflect ______.'",
}


def render_discoveries(data, guidance_mode, discovery_chart, guidance_box):
    """Render the discoveries tab using shared application services."""
    st.header("How have exoplanets been discovered?")
    guidance_box(
        guidance_mode,
        DISCOVERY_GUIDANCE["summary"],
        DISCOVERY_GUIDANCE["teacher"],
    )
    methods = sorted(data["discoverymethod"].dropna().unique().tolist())
    selected_methods = st.multiselect("Discovery methods", methods, default=methods)
    if selected_methods:
        st.plotly_chart(discovery_chart(data, selected_methods), use_container_width=True)
    else:
        st.warning("Select at least one discovery method.")
    if guidance_mode != "Minimal":
        st.markdown(DISCOVERY_GUIDANCE["prompt"])


def render_dataset(data, guidance_mode, field_options, variables, guidance_box, variable_card, scale_guidance):
    """Render the dataset tab using shared application services."""
    st.header("Meet the variables and dataset")
    guidance_box(
        guidance_mode,
        "Start with the variables you might use to describe a planet. Then inspect how those variables are recorded in the dataset.",
        "Learning intention: students distinguish a question-friendly variable name from the archive field used to store it, and recognise that missing values limit which questions can be answered.",
    )
    st.subheader("1. Variables we can use")
    st.write("The student-friendly name describes the idea. The NASA archive field is the short name used in the original data table.")
    variable_rows = [{"Variable": label, "NASA archive field": field, "What it tells us": variables.get(field, {}).get("description", "")} for label, field in DATASET_FIELDS]
    st.dataframe(pd.DataFrame(variable_rows), use_container_width=True, hide_index=True)
    selected_label = st.selectbox("Choose a variable to explore", list(field_options), key="dictionary_variable")
    variable_card(data, field_options[selected_label], guidance_mode, variables, scale_guidance)
    st.subheader("2. The dataset")
    st.write("Each row is one known exoplanet record. This is a sample of what astronomers have measured so far—not a list of every planet that exists.")
    display = [field for _, field in DATASET_FIELDS]
    friendly_columns = {field: label for label, field in DATASET_FIELDS}
    st.dataframe(data[display].rename(columns=friendly_columns), use_container_width=True, hide_index=True)
    st.subheader("3. What is missing?")
    st.write("A blank value means that property has not been recorded for that planet. It does not mean zero or that the property does not exist.")
    missing = pd.DataFrame({
        "Variable": display,
        "Missing records": [int(data[col].isna().sum()) for col in display],
        "Complete records (%)": [round(100 * data[col].notna().mean(), 1) for col in display],
    }).sort_values("Complete records (%)")
    st.dataframe(missing, use_container_width=True, hide_index=True)
    if guidance_mode != "Minimal":
        st.info("Missing means unknown. It does not mean zero, unsuitable, or evidence that a planet meets a criterion.")


def render_map(data, guidance_mode, sky_map):
    """Render the celestial map with the same colour choices as Three variables."""
    st.header("Celestial map")
    st.write("Each point shows a known exoplanet's direction in the sky. Use colour to look for patterns in another variable.")
    colour_options = ["No colour grouping", "Discovery method", "Discovery year"] + [f"{label} group" for label in PHYSICAL_GROUPS]
    colour_label = st.selectbox("Colour points by", colour_options, key="lab_map_colour")
    map_data = data.copy()
    colour_field = None
    if colour_label.endswith(" group"):
        group_label = colour_label.removesuffix(" group")
        group_field, breaks, labels = PHYSICAL_GROUPS[group_label]
        colour_field = "_map_colour_group"
        map_data[colour_field] = pd.cut(map_data[group_field], bins=breaks, labels=labels, include_lowest=True)
    elif colour_label == "Discovery method":
        colour_field = "discoverymethod"
    elif colour_label == "Discovery year":
        colour_field = "disc_year"
    mapped = map_data.dropna(subset=["x", "y", "z"])
    if guidance_mode != "Minimal":
        st.info(f"The map uses celestial direction for {len(mapped):,} records. It shows where systems appear in the sky, not their physical separation.")
    st.plotly_chart(sky_map(map_data, None, colour_field, colour_label), use_container_width=True)
    st.caption("The three directions are a way to display position on the sky. They are not distances or physical axes through space.")
    if guidance_mode == "Teacher":
        with st.expander("Teacher guidance", expanded=False):
            st.write("The points are placed using direction on the celestial sphere. Distance is deliberately not used to position them, so a nearby star and a distant star can appear in the same sky region.")


INVESTIGATIONS = {
    "Does planet size relate to mass?": {
        "x": "pl_rade", "y": "pl_bmasse", "colour": "discoverymethod",
        "log_x": False, "log_y": True,
        "question": "Do larger planets tend to have greater mass?",
        "caution": "Planets with similar radii can have very different compositions and masses. Mass is also missing for many planets.",
        "teacher": "Ask why two planets with similar radii might have different masses. Listen for composition, density and measurement uncertainty.",
    },
    "Does orbital distance relate to temperature?": {
        "x": "pl_orbsmax", "y": "pl_eqt", "colour": "discoverymethod",
        "log_x": True, "log_y": False,
        "question": "Are planets farther from their stars generally cooler?",
        "caution": "The host star's luminosity and the assumptions used in estimating equilibrium temperature also matter.",
        "teacher": "Use this to distinguish a broad relationship from a complete causal model. Distance is important, but it is not the only factor.",
    },
    "Do discovery methods reveal different planet populations?": {
        "x": "pl_orbper", "y": "pl_rade", "colour": "discoverymethod",
        "log_x": True, "log_y": False,
        "question": "Do discovery methods tend to identify planets with different sizes or orbital periods?",
        "caution": "Visible clusters may reflect detection bias as much as the underlying population of planets.",
        "teacher": "Prompt students to separate 'what exists' from 'what our instruments are good at finding'.",
    },
    "Has the reach of exoplanet discovery changed over time?": {
        "x": "disc_year", "y": "sy_dist", "colour": "discoverymethod",
        "log_x": False, "log_y": True,
        "question": "Have discoveries extended to more distant systems over time?",
        "caution": "Distance alone is not a simple measure of telescope capability or scientific progress.",
        "teacher": "Ask students what other factors influence the visible pattern, including survey design, methods and target selection.",
    },
}


def render(
    data,
    guidance_mode,
    *,
    teacher_note,
    step_tabs,
    scroll_to_top_if_requested,
    step_buttons,
    guidance_box,
    field_options,
    variables,
    variable_card,
    scale_guidance,
    sky_map,
):
    """Render the complete Data Laboratory experience using shared services."""
    heading, activity_controls = st.columns([4, 2])
    with heading:
        st.title(TITLE)
        st.caption(SUBTITLE)
    with activity_controls:
        st.toggle("Teacher view", key="lab_teacher_view", help="Show additional guidance for teaching and facilitating the investigation.")
    if guidance_mode == "Teacher":
        teacher_note(
            TEACHER_GUIDANCE["title"],
            TEACHER_GUIDANCE["purpose"],
            TEACHER_GUIDANCE["approach"],
            alignment=TEACHER_GUIDANCE["alignment"],
            timing=TEACHER_GUIDANCE["timing"],
            listen_for=TEACHER_GUIDANCE["listen_for"],
        )
    current_tab = int(st.session_state.get("lab_tab_step", 0))
    tabs, selected_tab = step_tabs(TAB_LABELS, "lab_tab", current_tab)
    if selected_tab != current_tab:
        current_tab = selected_tab
        st.session_state["lab_tab_step"] = current_tab
    scroll_to_top_if_requested("lab_scroll_to_top")
    if current_tab == 0:
        with tabs[0]:
            render_intro(data, guidance_mode, guidance_box)
    elif current_tab == 1:
        with tabs[1]:
            render_variables(data, guidance_mode, field_options, variables, variable_card, scale_guidance)
    elif current_tab == 2:
        with tabs[2]:
            render_dataset_and_missing(data, guidance_mode)
    elif current_tab == 3:
        with tabs[3]:
            render_one_variable(data, guidance_mode, field_options)
    elif current_tab == 4:
        with tabs[4]:
            render_two_variables(data, guidance_mode, field_options)
    elif current_tab == 5:
        with tabs[5]:
            render_three_variables(data, guidance_mode, field_options)
    else:
        with tabs[6]:
            render_map(data, guidance_mode, sky_map)
    step_buttons(TAB_LABELS, "lab_tab", "lab_tab_step", "lab_scroll_to_top", current_tab, "lab")

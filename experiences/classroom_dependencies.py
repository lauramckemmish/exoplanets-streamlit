"""Build pathway-specific lesson dependencies from shared classroom resources."""

from experiences import planets_we_have_not_found, strange_new_worlds


def render_lesson(data, pathway, part, stage4_pathway, stage5_pathway, resources):
    """Render a classroom lesson using the dependencies required by its pathway."""
    if pathway == stage4_pathway:
        dependencies = strange_new_worlds.LessonDependencies(
            pathway_name=stage4_pathway,
            exoplanet_image_path=resources["exoplanet_image_path"],
            solar_system_image_path=resources["solar_system_image_path"],
            planetary_systems_image_path=resources["planetary_systems_image_path"],
            nasa_kepler_16b_poster_path=resources["nasa_kepler_16b_poster_path"],
            nasa_51_pegasi_b_poster_path=resources["nasa_51_pegasi_b_poster_path"],
            nasa_kepler_186f_poster_path=resources["nasa_kepler_186f_poster_path"],
            solar_system_demographics_chart=resources["solar_system_demographics_chart"],
            planet_mass_distribution_chart=resources["planet_mass_distribution_chart"],
            discoveries_by_year_chart=resources["discoveries_by_year_chart"],
            current_demographics_chart=resources["current_demographics_chart"],
            graph_guide=resources["graph_guide"],
            graph_questions=resources["graph_questions"],
            response_box=resources["response_box"],
            key_idea=resources["key_idea"],
            log_scale_reveal=resources["log_scale_reveal"],
            data_detective_challenge=resources["data_detective_challenge"],
            learn_more_prompt=resources["learn_more_prompt"],
        )
        return strange_new_worlds.render_lesson(data, part, dependencies)

    if pathway == stage5_pathway:
        dependencies = planets_we_have_not_found.LessonDependencies(
            pathway_name=stage5_pathway,
            exoplanet_image_path=resources["exoplanet_image_path"],
            planetary_systems_image_path=resources["planetary_systems_image_path"],
            exoplanet_quadrants_image_path=resources["exoplanet_quadrants_image_path"],
            direct_imaging_image_path=resources["direct_imaging_image_path"],
            transit_detection_image_path=resources["transit_detection_image_path"],
            solar_system_demographics_chart=resources["solar_system_demographics_chart"],
            planet_mass_distribution_chart=resources["planet_mass_distribution_chart"],
            current_demographics_chart=resources["current_demographics_chart"],
            demographics_methods_chart=resources["demographics_methods_chart"],
            demographics_question=resources["demographics_question"],
            graph_guide=resources["graph_guide"],
            graph_questions=resources["graph_questions"],
            response_box=resources["response_box"],
            key_idea=resources["key_idea"],
            log_scale_reveal=resources["log_scale_reveal"],
            data_detective_challenge=resources["data_detective_challenge"],
            learn_more_prompt=resources["learn_more_prompt"],
        )
        return planets_we_have_not_found.render_lesson(data, part, dependencies)

    raise ValueError(f"Unknown classroom pathway: {pathway}")

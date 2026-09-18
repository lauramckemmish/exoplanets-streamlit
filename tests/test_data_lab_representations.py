"""Focused representation and chart-population checks for Exoplanet Data Lab."""

import inspect

import pandas as pd
import pytest

from charts import categorical_bar, count_heatmap, grouped_boxplot, histogram, scatter
from experiences import data_laboratory
from experiences.data_lab_fields import (
    DATA_LAB_FIELDS,
    DataLabField,
    chart_population,
    data_lab_fields,
    meaningful_range_counts,
    numeric_summary,
    one_variable_representations,
    pair_rejection_reason,
    representation_for_fields,
)


def _data() -> pd.DataFrame:
    return pd.DataFrame({
        "pl_name": ["A", "B", "C", "D"],
        "pl_bmasse": [1.0, None, 100.0, 0.0],
        "pl_rade": [1.0, 2.0, None, 4.0],
        "pl_eqt": [300.0, 500.0, None, 700.0],
        "discoverymethod": ["Transit", "Transit", "Imaging", None],
    })


def test_numeric_one_variable_uses_a_histogram_and_raw_unit_summary():
    data = _data()
    population = chart_population(data, ["pl_bmasse"])
    figure = histogram(population.data, "pl_bmasse", label="Planet mass (Earth masses)")

    assert DATA_LAB_FIELDS["pl_bmasse"].kind == "numeric"
    assert figure.data[0].type == "histogram"
    assert numeric_summary(data, "pl_bmasse") == {
        "usable": 3,
        "missing": 1,
        "minimum": 0.0,
        "median": 1.0,
        "mean": pytest.approx(33.6666666667),
        "maximum": 100.0,
    }


def test_numeric_fields_default_to_equal_ranges_and_only_configured_fields_offer_orders_of_magnitude():
    assert one_variable_representations("pl_bmasse")[0] == "equal_ranges"
    assert "orders_of_magnitude" in one_variable_representations("pl_bmasse")
    assert "orders_of_magnitude" not in one_variable_representations("disc_year")
    assert one_variable_representations("discoverymethod") == ()


def test_categorical_one_variable_uses_a_raw_count_bar_chart():
    data = _data()
    population = chart_population(data, ["discoverymethod"])
    counts = population.data["discoverymethod"].value_counts().rename_axis("Category").reset_index(name="Count")
    figure = categorical_bar(counts, label="Discovery method")

    assert DATA_LAB_FIELDS["discoverymethod"].kind == "categorical"
    assert figure.data[0].type == "bar"
    assert int(counts["Count"].sum()) == 3


def test_ineligible_identifiers_and_high_cardinality_categories_are_not_offered():
    data = _data().copy()
    data["discoverymethod"] = [f"method-{index}" for index in range(len(data))]

    fields = data_lab_fields(data, eligibility="one_variable")
    assert "pl_name" not in fields
    assert "discoverymethod" in fields

    oversized = pd.concat([data] * 4, ignore_index=True)
    oversized["discoverymethod"] = [f"method-{index}" for index in range(len(oversized))]
    assert "discoverymethod" not in data_lab_fields(oversized, eligibility="one_variable")


def test_log_display_is_explicit_and_raw_summary_does_not_change():
    data = pd.DataFrame({"pl_bmasse": [0.1, 1.0, 10.0, None]})
    summary = numeric_summary(data, "pl_bmasse")
    population = chart_population(data, ["pl_bmasse"], log_fields=["pl_bmasse"])
    figure = histogram(population.data, "pl_bmasse", label="Planet mass", log_x=True)

    assert DATA_LAB_FIELDS["pl_bmasse"].log_eligible
    assert not DATA_LAB_FIELDS["pl_eqt"].log_eligible
    assert figure.layout.xaxis.type == "log"
    assert summary["minimum"] == 0.1
    assert summary["maximum"] == 10.0


def test_orders_of_magnitude_histogram_uses_log_spaced_bins():
    data = pd.DataFrame({"pl_bmasse": [1.0, 10.0, 100.0, 1000.0]})
    figure = histogram(data, "pl_bmasse", label="Planet mass", log_x=True)
    centres = list(figure.data[0].x)

    assert figure.data[0].type == "bar"
    assert figure.layout.xaxis.type == "log"
    assert centres[1] / centres[0] == pytest.approx(centres[2] / centres[1])


def test_one_variable_chart_population_separates_missing_and_log_exclusions():
    data = _data()

    standard = chart_population(data, ["pl_bmasse"])
    logged = chart_population(data, ["pl_bmasse"], log_fields=["pl_bmasse"])
    categorical = chart_population(data, ["discoverymethod"])

    assert (len(standard.data), standard.total, standard.missing, standard.log_excluded) == (3, 4, 1, 0)
    assert (len(logged.data), logged.total, logged.missing, logged.log_excluded) == (2, 4, 1, 1)
    assert (len(categorical.data), categorical.total, categorical.missing) == (3, 4, 1)


def test_meaningful_ranges_are_explicit_and_keep_configured_order_and_counts():
    data = pd.DataFrame({"pl_bmasse": [0.5, 2.0, 50.0, 500.0, 2000.0, None]})
    counts = meaningful_range_counts(data.dropna(subset=["pl_bmasse"]), "pl_bmasse")

    assert "meaningful_ranges" in one_variable_representations("pl_bmasse")
    assert "meaningful_ranges" not in one_variable_representations("pl_orbper")
    assert counts["Category"].tolist() == list(DATA_LAB_FIELDS["pl_bmasse"].meaningful_range_labels)
    assert counts["Count"].tolist() == [1, 1, 1, 1, 1]


def test_two_numeric_variables_use_scatter_with_independent_log_axes():
    data = _data()
    population = chart_population(data, ["pl_rade", "pl_bmasse"])
    figure = scatter(
        population.data, "pl_rade", "pl_bmasse", x_label="Planet radius", y_label="Planet mass",
        log_x=False, log_y=True,
    )

    assert representation_for_fields("pl_rade", "pl_bmasse") == "scatter"
    assert figure.data[0].type == "scatter"
    assert figure.layout.xaxis.type is None
    assert figure.layout.yaxis.type == "log"


def test_categorical_numeric_variables_use_grouped_boxplots():
    data = _data()
    population = chart_population(data, ["discoverymethod", "pl_eqt"])
    figure = grouped_boxplot(
        population.data, "discoverymethod", "pl_eqt", category_label="Discovery method",
        numeric_label="Equilibrium temperature (K)", log_y=False,
    )

    assert representation_for_fields("discoverymethod", "pl_eqt") == "grouped_boxplot"
    assert figure.data[0].type == "box"
    assert (len(population.data), population.missing) == (2, 2)


def test_categorical_pairs_use_an_annotated_raw_count_heatmap_with_zeroes():
    metadata = {
        "method": DataLabField("method", "Method", "categorical", "A method.", "discovery/context metadata", True, True),
        "context": DataLabField("context", "Context", "categorical", "A context.", "discovery/context metadata", True, True),
    }
    data = pd.DataFrame({"method": ["Transit", "Imaging"], "context": ["Near", "Far"]})
    figure = count_heatmap(data, "method", "context", x_label="Method", y_label="Context")

    assert representation_for_fields("method", "context", metadata=metadata) == "count_heatmap"
    assert figure.data[0].type == "heatmap"
    assert 0 in figure.data[0].z.flatten()
    assert "0" in {annotation.text for annotation in figure.layout.annotations}


def test_two_variable_population_omits_rows_missing_either_required_value():
    population = chart_population(_data(), ["pl_rade", "pl_bmasse"])

    assert population.total == 4
    assert population.missing == 2
    assert len(population.data) == 2


def test_pair_rejection_remains_a_lightweight_local_guardrail():
    rejected = {("pl_bmasse", "pl_rade"): "This local comparison needs a different representation."}

    assert pair_rejection_reason("pl_rade", "pl_bmasse", pair_rejections=rejected) == (
        "This local comparison needs a different representation."
    )


def test_no_fitted_model_equation_or_r_squared_is_added_to_data_lab():
    source = inspect.getsource(data_laboratory.render_two_variables).lower()

    assert "trendline" not in source
    assert "r²" not in source
    assert "r2" not in source
    assert "equation" not in source

"""Focused checks for the Exoplanet Data Laboratory field-capability adapter."""

import pandas as pd
import pytest

from experiences import data_laboratory
from experiences.data_lab_fields import (
    DATA_LAB_FIELDS,
    FIELD_KINDS,
    DataLabField,
    data_lab_fields,
    data_lab_grouping_fields,
    data_lab_subset_fields,
    legacy_field_options,
    legacy_variables,
    pair_rejection_reason,
    source_missingness,
    validate_data_lab_fields,
)


def _configured_frame() -> pd.DataFrame:
    return pd.DataFrame({name: [1, None] for name in DATA_LAB_FIELDS})


def test_every_configured_data_lab_field_has_valid_complete_metadata():
    validate_data_lab_fields()

    assert set(DATA_LAB_FIELDS) == {field.name for field in DATA_LAB_FIELDS.values()}
    for field in DATA_LAB_FIELDS.values():
        assert field.kind in FIELD_KINDS
        assert field.label
        assert field.meaning
        assert field.role


def test_identifiers_cannot_accidentally_become_generic_graph_choices():
    frame = _configured_frame()
    choices = data_lab_fields(frame, eligibility="one_variable") + data_lab_fields(frame, eligibility="two_variable")

    assert "pl_name" not in choices
    assert "hostname" not in choices


def test_graph_and_log_eligibility_are_explicit_not_dtype_inference():
    frame = _configured_frame()

    assert "disc_year" in data_lab_fields(frame, eligibility="one_variable")
    assert DATA_LAB_FIELDS["disc_year"].kind == "numeric"
    assert not DATA_LAB_FIELDS["disc_year"].log_eligible
    assert DATA_LAB_FIELDS["pl_bmasse"].log_eligible
    assert not DATA_LAB_FIELDS["sy_snum"].log_eligible


def test_discovery_method_is_the_only_initial_grouping_and_subset_capability():
    frame = _configured_frame()

    assert DATA_LAB_FIELDS["discoverymethod"].one_variable
    assert DATA_LAB_FIELDS["discoverymethod"].two_variable
    assert data_lab_grouping_fields(frame) == ["discoverymethod"]
    assert data_lab_subset_fields(frame) == ["discoverymethod"]


def test_source_missingness_is_calculated_from_the_whole_prepared_catalogue():
    frame = pd.DataFrame({"pl_eqt": [300.0, None, None, 450.0]})

    assert source_missingness(frame, "pl_eqt") == {
        "missing_count": 2,
        "missing_percentage": 50.0,
    }


def test_existing_data_lab_missing_table_uses_source_level_metadata():
    frame = pd.DataFrame({
        "pl_name": ["A", "B"], "hostname": ["Star A", None],
        "disc_year": [2020, 2021], "discoverymethod": ["Transit", "Transit"],
        "pl_rade": [1.0, None], "pl_bmasse": [1.0, 2.0], "pl_orbper": [2.0, 3.0],
        "pl_eqt": [300.0, None], "sy_dist": [10.0, 20.0],
        "sy_snum": [1, 1], "sy_pnum": [1, None],
    })

    table = data_laboratory.source_missing_table(
        frame, [field for _, field in data_laboratory.DATASET_FIELDS]
    )

    temperature = table.loc[table["Variable"] == "Equilibrium temperature (K)"].iloc[0]
    assert temperature["Missing records"] == 1
    assert temperature["Complete records (%)"] == 50.0


def test_pair_rejection_is_a_small_local_escape_hatch_not_a_rule_engine():
    rejected = {("disc_year", "pl_eqt"): "Use discovery context separately from this physical comparison."}

    assert pair_rejection_reason("pl_eqt", "disc_year", pair_rejections=rejected) == (
        "Use discovery context separately from this physical comparison."
    )
    assert pair_rejection_reason("pl_eqt", "pl_rade", pair_rejections=rejected) is None


@pytest.mark.parametrize("kind", ["identifier", "non-plottable"])
def test_identifier_or_non_plottable_graph_configuration_is_rejected(kind):
    invalid = DataLabField(
        "record", "Record", kind, "A non-analytical field.", "identifier", True, False
    )

    with pytest.raises(ValueError, match="cannot be a generic graph choice"):
        validate_data_lab_fields({"record": invalid})


def test_existing_data_lab_labels_and_stage_order_remain_compatible():
    variables = legacy_variables()

    assert list(data_laboratory.TAB_LABELS) == [
        "Start here", "Variables", "Dataset and missing values", "One variable",
        "Two variables", "Three variables", "Sky map",
    ]
    assert legacy_field_options()["Planet mass (Earth masses)"] == "pl_bmasse"
    assert variables["pl_eqt"]["measurement"].startswith("Calculated estimate")
    assert variables["pl_rade"]["log"] == "optional"
    assert variables["sy_snum"]["log"] == "not suitable"
    assert data_laboratory.DATASET_FIELDS == [
        ("Planet name", "pl_name"), ("Host star", "hostname"),
        ("Discovery year", "disc_year"), ("Discovery method", "discoverymethod"),
        ("Planet radius (Earth radii)", "pl_rade"),
        ("Planet mass (Earth masses)", "pl_bmasse"),
        ("Orbital period (days)", "pl_orbper"), ("Equilibrium temperature (K)", "pl_eqt"),
        ("Distance from Earth (light-years)", "sy_dist"),
        ("Known stars in system", "sy_snum"), ("Known planets in system", "sy_pnum"),
    ]

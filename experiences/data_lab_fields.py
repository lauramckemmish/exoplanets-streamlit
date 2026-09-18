"""Explicit, local field capabilities for the Exoplanet Data Laboratory.

This adapter is deliberately owned by Data Lab.  It records learner-facing
meaning and analytical choices for this experience; it is not a repository-wide
catalogue schema and does not alter other experiences' missing-data semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping

import pandas as pd


FieldKind = Literal["numeric", "categorical", "identifier", "non-plottable"]
FIELD_KINDS = frozenset({"numeric", "categorical", "identifier", "non-plottable"})
FIELD_ROLES = frozenset({"identifier", "planet property", "host/system context", "discovery/context metadata"})


@dataclass(frozen=True)
class DataLabField:
    """One configured Data Lab field and its explicitly chosen capabilities."""

    name: str
    label: str
    kind: FieldKind
    meaning: str
    role: str
    one_variable: bool
    two_variable: bool
    unit: str | None = None
    log_eligible: bool = False
    grouping_eligible: bool = False
    subset_eligible: bool = False
    category_order: tuple[str, ...] | None = None
    measurement: str | None = None
    log_guidance: str | None = None
    log_status: str | None = None
    dataset_label: str | None = None

    @property
    def option_label(self) -> str:
        return f"{self.label} ({self.unit})" if self.unit else self.label

    @property
    def table_label(self) -> str:
        return self.dataset_label or self.option_label


# This is the Data Lab's single source of field truth.  Coordinates are
# technical map inputs, not learner-facing data fields, so they stay out of
# this adapter.  The prepared catalogue owns their derivation.
DATA_LAB_FIELDS: dict[str, DataLabField] = {
    "pl_name": DataLabField(
        "pl_name", "Planet name", "identifier", "The catalogue name used to identify one confirmed planet record.",
        "identifier", False, False, dataset_label="Planet name",
    ),
    "hostname": DataLabField(
        "hostname", "Host star", "identifier", "The star named as the host of this planet record.",
        "host/system context", False, False, dataset_label="Host star",
    ),
    "disc_year": DataLabField(
        "disc_year", "Discovery year", "numeric", "The calendar year the planet was reported as discovered.",
        "discovery/context metadata", True, True, "year", measurement="A calendar year, not a physical measurement.",
        log_guidance="Equal differences between years are meaningful, so a linear axis is clearer.", dataset_label="Discovery year",
    ),
    "discoverymethod": DataLabField(
        "discoverymethod", "Discovery method", "categorical", "The observing method used to detect or confirm the planet.",
        "discovery/context metadata", True, True, grouping_eligible=True, subset_eligible=True, dataset_label="Discovery method",
    ),
    "pl_rade": DataLabField(
        "pl_rade", "Planet radius", "numeric", "The size of the planet compared with Earth.",
        "planet property", True, True, "Earth radii", True,
        measurement="Measured or modelled from observations, often from transit data.",
        log_guidance="Radius varies substantially, but usually across fewer orders of magnitude than mass or orbital period.",
        log_status="optional", dataset_label="Planet radius (Earth radii)",
    ),
    "pl_bmasse": DataLabField(
        "pl_bmasse", "Planet mass", "numeric", "The mass of the planet compared with Earth.",
        "planet property", True, True, "Earth masses", True,
        measurement="Measured or estimated from methods such as radial velocity and transit timing.",
        log_guidance="Planet masses span many orders of magnitude, so a logarithmic axis usually reveals the structure more clearly.",
        dataset_label="Planet mass (Earth masses)",
    ),
    "pl_orbper": DataLabField(
        "pl_orbper", "Orbital period", "numeric", "The time taken for the planet to complete one orbit around its host star.",
        "planet property", True, True, "days", True,
        measurement="Measured from repeating signals such as transits or radial-velocity cycles.",
        log_guidance="Orbital periods range from fractions of a day to many years.", dataset_label="Orbital period (days)",
    ),
    "pl_orbsmax": DataLabField(
        "pl_orbsmax", "Orbital distance", "numeric", "A measure of the planet's orbital distance from its host star.",
        "planet property", True, True, "astronomical units (AU)", True,
        measurement="Calculated from orbital observations and system models.",
        log_guidance="Orbital distances span very small to very large values.",
    ),
    "pl_eqt": DataLabField(
        "pl_eqt", "Equilibrium temperature", "numeric", "An estimate of the planet's temperature based on absorbed and emitted radiation.",
        "planet property", True, True, "kelvin (K)", False,
        measurement="Calculated estimate. It does not directly represent surface temperature or climate.",
        log_guidance="Temperature values are positive but normally occupy a range that remains readable on a linear axis.",
        dataset_label="Equilibrium temperature (K)",
    ),
    "sy_dist": DataLabField(
        "sy_dist", "Distance from Earth", "numeric", "The distance from Earth to the planetary system.",
        "host/system context", True, True, "light-years", True,
        measurement="Measured astronomically, commonly using parallax and related methods.",
        log_guidance="Distances span a broad range and may cluster near the lower end on a linear axis.", dataset_label="Distance from Earth (light-years)",
    ),
    "sy_snum": DataLabField(
        "sy_snum", "Stars in system", "numeric", "The number of known stars in the planetary system.",
        "host/system context", True, True, "count", False,
        measurement="A small whole-number count.",
        log_guidance="Small category-like counts are clearer on a linear axis.",
        log_status="not suitable", dataset_label="Known stars in system",
    ),
    "sy_pnum": DataLabField(
        "sy_pnum", "Planets in system", "numeric", "The number of known planets in the planetary system.",
        "host/system context", True, True, "count", False,
        measurement="A small whole-number count that may change as more planets are discovered.",
        log_guidance="Small whole-number counts are clearer on a linear axis.",
        log_status="not suitable", dataset_label="Known planets in system",
    ),
}

# A local escape hatch for a future, specifically misleading pair.  It is
# intentionally empty: Data Lab has not yet identified a pair to suppress.
DATA_LAB_PAIR_REJECTIONS: dict[tuple[str, str], str] = {}


def validate_data_lab_fields(metadata: Mapping[str, DataLabField] = DATA_LAB_FIELDS) -> None:
    """Reject incomplete or contradictory local capability configuration."""
    for configured_name, field in metadata.items():
        if configured_name != field.name:
            raise ValueError(f"Data Lab field key {configured_name!r} must match its internal name.")
        if not field.label or not field.meaning or not field.role:
            raise ValueError(f"Data Lab field {field.name!r} requires label, meaning, and role.")
        if field.kind not in FIELD_KINDS:
            raise ValueError(f"Data Lab field {field.name!r} has an invalid kind: {field.kind!r}.")
        if field.role not in FIELD_ROLES:
            raise ValueError(f"Data Lab field {field.name!r} has an invalid role: {field.role!r}.")
        if field.kind in {"identifier", "non-plottable"} and (field.one_variable or field.two_variable):
            raise ValueError(f"{field.kind} field {field.name!r} cannot be a generic graph choice.")
        if field.log_eligible and field.kind != "numeric":
            raise ValueError(f"Only numeric Data Lab field {field.name!r} can be log eligible.")
        if (field.grouping_eligible or field.subset_eligible) and field.kind != "categorical":
            raise ValueError(f"Only categorical Data Lab field {field.name!r} can group or subset records.")


def data_lab_fields(data: pd.DataFrame, *, eligibility: Literal["one_variable", "two_variable"]) -> list[str]:
    """Return configured graph choices; never infer eligibility from dtype."""
    validate_data_lab_fields()
    return [
        field.name for field in DATA_LAB_FIELDS.values()
        if field.name in data.columns and getattr(field, eligibility)
    ]


def data_lab_grouping_fields(data: pd.DataFrame) -> list[str]:
    """Return explicitly configured categorical grouping fields present in data."""
    validate_data_lab_fields()
    return [field.name for field in DATA_LAB_FIELDS.values() if field.name in data.columns and field.grouping_eligible]


def data_lab_subset_fields(data: pd.DataFrame) -> list[str]:
    """Return explicitly configured categorical subset fields present in data."""
    validate_data_lab_fields()
    return [field.name for field in DATA_LAB_FIELDS.values() if field.name in data.columns and field.subset_eligible]


def source_missingness(data: pd.DataFrame, field: str) -> dict[str, int | float]:
    """Calculate source-level missingness from the whole prepared catalogue."""
    missing_count = int(data[field].isna().sum())
    total = len(data)
    return {
        "missing_count": missing_count,
        "missing_percentage": 0.0 if total == 0 else missing_count / total * 100,
    }


def canonical_pair(first: str, second: str) -> tuple[str, str]:
    """Return a stable local key for a potential pair-specific warning."""
    return tuple(sorted((first, second)))


def pair_rejection_reason(
    first: str,
    second: str,
    *,
    pair_rejections: Mapping[tuple[str, str], str] | None = None,
) -> str | None:
    """Return a configured local pair warning without deriving scientific rules."""
    rejections = DATA_LAB_PAIR_REJECTIONS if pair_rejections is None else pair_rejections
    return rejections.get(canonical_pair(first, second))


def legacy_variables() -> dict[str, dict[str, str]]:
    """Provide the existing Data Lab variable-card interface from this adapter."""
    return {
        field.name: {
            "label": field.label,
            "unit": field.unit or "",
            "description": field.meaning,
            "measurement": field.measurement or "",
            "log": field.log_status or ("recommended" if field.log_eligible else "usually unnecessary"),
            "log_reason": field.log_guidance or "A logarithmic display is not configured for this field.",
        }
        for field in DATA_LAB_FIELDS.values()
        if field.one_variable and field.kind == "numeric"
    }


def legacy_field_options() -> dict[str, str]:
    """Provide the existing selectbox labels from the local field adapter."""
    return {
        field.option_label: field.name
        for field in DATA_LAB_FIELDS.values()
        if field.one_variable and field.kind == "numeric"
    }

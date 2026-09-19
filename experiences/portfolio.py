"""Portable portfolio identifiers and launch mapping for Planets Beyond.

This module deliberately translates stable public IDs into the existing local
catalogue destinations.  It does not expose local route or pathway values in
the portable manifest.
"""

from __future__ import annotations

from dataclasses import dataclass


PUBLIC_APP_URL = "https://exoplanets-curious-2026.streamlit.app"
PUBLIC_QUERY_PARAMETER = "experience"


@dataclass(frozen=True)
class PortfolioDestination:
    """One public ID and the catalogue entry it launches."""

    experience_id: str
    catalogue_name: str
    collection: str


DESTINATIONS = (
    PortfolioDestination(
        "planets-beyond/planet-shopping-outside-our-solar-system",
        "Planet Shopping Outside Our Solar System",
        "experience",
    ),
    PortfolioDestination(
        "planets-beyond/is-our-solar-system-normal",
        "Is Our Solar System Normal?",
        "experience",
    ),
    PortfolioDestination(
        "planets-beyond/strange-new-worlds",
        "Strange New Worlds",
        "experience",
    ),
    PortfolioDestination(
        "planets-beyond/the-planets-we-havent-found",
        "The Planets We Haven't Found",
        "experience",
    ),
    PortfolioDestination(
        "planets-beyond/exoplanet-data-lab",
        "Exoplanet Data Lab",
        "explore",
    ),
)

_DESTINATIONS_BY_ID = {destination.experience_id: destination for destination in DESTINATIONS}


def destination_for_id(experience_id: str | None) -> PortfolioDestination | None:
    """Return the public destination for one stable ID, if it is published."""
    if not isinstance(experience_id, str):
        return None
    return _DESTINATIONS_BY_ID.get(experience_id)


def launch_url(experience_id: str) -> str:
    """Return the canonical public launch URL for a published stable ID."""
    if destination_for_id(experience_id) is None:
        raise ValueError(f"Unknown portfolio experience ID: {experience_id}")
    return f"{PUBLIC_APP_URL}/?{PUBLIC_QUERY_PARAMETER}={experience_id}"

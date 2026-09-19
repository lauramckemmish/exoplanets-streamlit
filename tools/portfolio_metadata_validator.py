"""Offline Data to Discovery portfolio manifest validation.

This is a compact, repository-local implementation of the v1 validator from
``data-experience-streamlit-starter`` commit
``9e0aa0d163c4a474721c768135e8c97187a51aec``.  It performs structural
validation only and deliberately makes no network requests.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from tools.portfolio_metadata_registry import GLOBAL_UMBRELLAS


SCHEMA_VERSION = "data-to-discovery/1.0"
ALLOWED_KINDS = {"guided_experience", "explore_resource"}
ALLOWED_STAGES = {"Early Stage 1", *(f"Stage {number}" for number in range(1, 7))}
ALLOWED_DELIVERY_MODES = {"facilitated", "classroom", "independent"}
ALLOWED_EVIDENCE_TYPES = {
    "observational_measurements", "scientific_catalogue", "curated_dataset",
    "derived_model", "simulation", "external_reference_data", "citizen_science",
}
ALLOWED_ALIGNMENTS = {"DIRECT", "PARTIAL", "POTENTIAL", "NOT_ADDRESSED"}
_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_EXPERIENCE_ID = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)/([a-z0-9]+(?:-[a-z0-9]+)*)$")
_FOCUS = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_PROGRAMME = re.compile(r"^[A-Z][A-Z0-9_]*$")
_OUTCOME = re.compile(r"^[A-Z]{2,6}[0-9]+(?:-[A-Z0-9]+)+$")
_CONTENT = re.compile(r"^[A-Z][A-Z0-9]*$")


def load_manifest(path: str | Path) -> Any:
    with Path(path).open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


def validate_manifest(manifest: Any) -> list[str]:
    """Return v1 structural validation errors without fetching URLs."""
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest must be an object"]
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    resource = manifest.get("resource")
    resource_id = _resource(resource, errors)
    experiences = manifest.get("experiences")
    if not isinstance(experiences, list):
        return errors + ["experiences must be a list"]
    seen: set[str] = set()
    for index, experience in enumerate(experiences):
        path = f"experiences[{index}]"
        experience_id = _experience(experience, resource_id, path, errors)
        if experience_id in seen:
            errors.append(f"{path}.experience_id duplicates {experience_id!r}")
        if experience_id:
            seen.add(experience_id)
    return errors


def _resource(resource: Any, errors: list[str]) -> str | None:
    if not isinstance(resource, dict):
        errors.append("resource must be an object")
        return None
    _keys(resource, ("resource_id", "title", "summary", "repository", "app_url"), "resource", errors)
    resource_id = resource.get("resource_id")
    if not _text(resource_id):
        errors.append("resource.resource_id must be a nonblank string")
    elif not _ID.fullmatch(resource_id):
        errors.append("resource.resource_id must use lowercase kebab case")
    for field in ("title", "summary"):
        if not _text(resource.get(field)):
            errors.append(f"resource.{field} must be a nonblank string")
    for field in ("repository", "app_url"):
        if not _https(resource.get(field)):
            errors.append(f"resource.{field} must be an HTTPS URL")
    return resource_id if isinstance(resource_id, str) else None


def _experience(value: Any, resource_id: str | None, path: str, errors: list[str]) -> str | None:
    required = ("experience_id", "title", "summary", "kind", "published", "stages", "duration_minutes", "science_focus", "data_science_focus", "curriculum", "umbrellas", "delivery_modes", "programmes", "evidence_types", "launch")
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return None
    _keys(value, required, path, errors)
    experience_id = value.get("experience_id")
    match = _EXPERIENCE_ID.fullmatch(experience_id) if isinstance(experience_id, str) else None
    if not match:
        errors.append(f"{path}.experience_id must be resource-id/experience-slug")
    elif resource_id and match.group(1) != resource_id:
        errors.append(f"{path}.experience_id must start with {resource_id!r}")
    for field in ("title", "summary"):
        if not _text(value.get(field)):
            errors.append(f"{path}.{field} must be a nonblank string")
    if value.get("kind") not in ALLOWED_KINDS:
        errors.append(f"{path}.kind must be one of {sorted(ALLOWED_KINDS)}")
    if not isinstance(value.get("published"), bool):
        errors.append(f"{path}.published must be a boolean")
    _list(value.get("stages"), f"{path}.stages", errors, allowed=ALLOWED_STAGES)
    _duration(value.get("duration_minutes"), f"{path}.duration_minutes", errors)
    _list(value.get("science_focus"), f"{path}.science_focus", errors, pattern=_FOCUS, nonempty=True)
    _list(value.get("data_science_focus"), f"{path}.data_science_focus", errors, pattern=_FOCUS, nonempty=True)
    _curriculum(value.get("curriculum"), f"{path}.curriculum", errors)
    _list(value.get("umbrellas"), f"{path}.umbrellas", errors, pattern=_ID)
    for umbrella in value.get("umbrellas", []) if isinstance(value.get("umbrellas"), list) else []:
        if umbrella not in GLOBAL_UMBRELLAS:
            errors.append(f"{path}.umbrellas contains unregistered global umbrella {umbrella!r}")
    _list(value.get("delivery_modes"), f"{path}.delivery_modes", errors, allowed=ALLOWED_DELIVERY_MODES)
    _list(value.get("programmes"), f"{path}.programmes", errors, pattern=_PROGRAMME)
    _list(value.get("evidence_types"), f"{path}.evidence_types", errors, allowed=ALLOWED_EVIDENCE_TYPES, nonempty=True)
    _launch(value.get("launch"), value.get("published"), f"{path}.launch", errors)
    return experience_id if isinstance(experience_id, str) else None


def _curriculum(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return
    for index, framework in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(framework, dict):
            errors.append(f"{item_path} must be an object")
            continue
        _keys(framework, ("framework", "outcomes"), item_path, errors)
        if not _text(framework.get("framework")):
            errors.append(f"{item_path}.framework must be a nonblank string")
        outcomes = framework.get("outcomes")
        if not isinstance(outcomes, list):
            errors.append(f"{item_path}.outcomes must be a list")
            continue
        for outcome_index, outcome in enumerate(outcomes):
            outcome_path = f"{item_path}.outcomes[{outcome_index}]"
            if not isinstance(outcome, dict):
                errors.append(f"{outcome_path} must be an object")
                continue
            _keys(outcome, ("outcome_code", "alignment", "detailed_content"), outcome_path, errors)
            code = outcome.get("outcome_code")
            if not isinstance(code, str) or not _OUTCOME.fullmatch(code):
                errors.append(f"{outcome_path}.outcome_code must use official NESA outcome-code syntax")
            if outcome.get("alignment") not in ALLOWED_ALIGNMENTS:
                errors.append(f"{outcome_path}.alignment must be an allowed alignment")
            details = outcome.get("detailed_content")
            if not isinstance(details, list):
                errors.append(f"{outcome_path}.detailed_content must be a list")
                continue
            for detail_index, detail in enumerate(details):
                detail_path = f"{outcome_path}.detailed_content[{detail_index}]"
                if not isinstance(detail, dict):
                    errors.append(f"{detail_path} must be an object")
                    continue
                _keys(detail, ("content_id", "alignment"), detail_path, errors)
                content_id = detail.get("content_id")
                if not isinstance(content_id, str) or not isinstance(code, str) or not content_id.startswith(f"{code}.") or not _CONTENT.fullmatch(content_id.removeprefix(f"{code}.")):
                    errors.append(f"{detail_path}.content_id must begin with its outcome code")
                if detail.get("alignment") not in ALLOWED_ALIGNMENTS:
                    errors.append(f"{detail_path}.alignment must be an allowed alignment")


def _duration(value: Any, path: str, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, dict) or set(value) != {"minimum", "maximum"}:
        errors.append(f"{path} must be null or contain only minimum and maximum")
        return
    minimum, maximum = value["minimum"], value["maximum"]
    if not all(isinstance(item, int) and not isinstance(item, bool) and item > 0 for item in (minimum, maximum)):
        errors.append(f"{path}.minimum and {path}.maximum must be positive integers")
    elif minimum > maximum:
        errors.append(f"{path}.minimum must be less than or equal to {path}.maximum")


def _launch(value: Any, published: Any, path: str, errors: list[str]) -> None:
    if published is True and (not isinstance(value, dict) or not _https(value.get("url"))):
        errors.append(f"{path}.url must be an HTTPS URL when published is true")
    if published is False and value is not None:
        errors.append(f"{path} must be null when published is false")


def _list(value: Any, path: str, errors: list[str], *, allowed: set[str] | None = None, pattern: re.Pattern[str] | None = None, nonempty: bool = False) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return
    if nonempty and not value:
        errors.append(f"{path} must not be empty")
    if len(value) != len(set(value)):
        errors.append(f"{path} must not contain duplicate values")
    for item in value:
        if not _text(item):
            errors.append(f"{path} values must be nonblank strings")
        elif allowed is not None and item not in allowed:
            errors.append(f"{path} contains invalid value {item!r}")
        elif pattern is not None and not pattern.fullmatch(item):
            errors.append(f"{path} contains invalid token {item!r}")


def _keys(value: dict[str, Any], keys: tuple[str, ...], path: str, errors: list[str]) -> None:
    for key in keys:
        if key not in value:
            errors.append(f"{path} is missing required key {key!r}")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _https(value: Any) -> bool:
    if not _text(value) or any(character.isspace() for character in value):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and parsed.username is None and parsed.password is None

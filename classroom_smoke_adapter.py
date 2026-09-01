"""Exoplanets route and burst interaction for classroom smoke testing."""

from __future__ import annotations

import sys
from pathlib import Path


class ExoplanetsClassroomAdapter:
    """Exercise the existing Planet Shopping Combine stage.

    The adapter uses the normal sidebar and stage-tab navigation. Each round
    makes one small distance-slider adjustment, a live learner interaction on
    Combine that updates the real shortlist calculation.
    """

    def streamlit_command(self, root: Path, port: int) -> list[str]:
        return [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            f"--server.port={port}",
            "--server.headless=true",
            "--server.fileWatcherType=none",
        ]

    async def arrive(self, page: object) -> None:
        await page.get_by_role("button", name="Planet Shopping").click(no_wait_after=True)
        await page.get_by_role("heading", name="Planet Shopping Outside Our Solar System", exact=True).wait_for()
        await page.get_by_role("tab", name="Combine", exact=True).click()
        await page.get_by_role("heading", name="Combine").wait_for()

    async def interact(self, page: object, round_number: int) -> None:
        await page.locator('input[type="range"]').first.press("ArrowRight")

    async def assert_usable(self, page: object) -> None:
        await page.get_by_role("heading", name="Combine").wait_for()
        await page.locator('input[type="range"]').first.wait_for()
        await page.get_by_text("Within the distance criterion", exact=True).wait_for()


ADAPTER = ExoplanetsClassroomAdapter()

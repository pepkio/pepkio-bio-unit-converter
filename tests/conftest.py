"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "bio-unit-converter",
        "title": "Bio Unit Converter",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "bsa_molarity",
                "input": {
                    "mode": "molarity",
                    "mass": 1,
                    "mass_unit": "ug",
                    "volume": 100,
                    "volume_unit": "uL",
                    "molecular_weight_g_per_mol": 66463,
                    "output_molar_unit": "nM",
                },
            },
            {
                "name": "dilution_solve_v1",
                "input": {
                    "mode": "dilution",
                    "c1": 10,
                    "c1_unit": "mM",
                    "c2": 1,
                    "c2_unit": "mM",
                    "v2": 1,
                    "v2_unit": "mL",
                },
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "mode": "dilution",
            "result": {"v1": 0.1, "v1_unit": "mL"},
            "warnings": [],
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }

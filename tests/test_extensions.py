"""Tests for the `extensions` module."""

from pathlib import Path

import pytest
import copier

TEMPLATES_DIRECTORY = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    ("template_name", "expected"),
    [
        ("template_not_using_loader", "not set"),
        ("template_using_loader", "True"),
        ("template_modifying_context", "True"),
    ]
)
def test_extension_loader(tmp_path, template_name, expected):
    template_path = TEMPLATES_DIRECTORY / template_name
    copier.copy(str(template_path), tmp_path)
    result_file = tmp_path / "result.txt"
    assert result_file.exists()
    assert result_file.read_text() == f"Success variable: {expected}"

"""Tests for the `extensions` module."""

from pathlib import Path

import copier
import pytest
from copier.errors import UserMessageError

TEMPLATES_DIRECTORY = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    ("template_name", "expected"),
    [
        ("not_using_loader", "not set"),
        ("using_loader", "True"),
        ("updating_context", "True"),
        ("modifying_context", "True"),
        ("not_updating_context_for_prompts", "True"),
        ("loading_normal_extension", "not set"),
    ],
)
def test_extensions(tmp_path, template_name, expected):
    """Test loader and context extensions.

    Arguments:
        tmp_path: A pytest fixture.
        template_name: The parametrized template to use.
        expected: The parametrized value we expect.
    """
    template_path = TEMPLATES_DIRECTORY / template_name
    copier.copy(str(template_path), tmp_path, defaults=True, overwrite=True)
    result_file = tmp_path / "result.txt"
    assert result_file.exists()
    assert result_file.read_text() == f"Success variable: {expected}"


@pytest.mark.parametrize(
    ("template_name", "exception"),
    [
        ("raising_exception_while_loading", RuntimeError),
        ("cant_find_extension_file", UserMessageError),
        ("cant_find_extension_class", UserMessageError),
        ("cant_find_extension_module", UserMessageError),
        ("cant_find_extension_package", UserMessageError),
    ],
)
def test_extensions_raising_exceptions(tmp_path, template_name, exception):
    """See what happens when an extension raises an exception.

    Arguments:
        tmp_path: A pytest fixture.
        template_name: The parametrized template to use.
        exception: The exception expected to be raised.
    """
    template_path = TEMPLATES_DIRECTORY / template_name
    with pytest.raises(exception):
        copier.copy(str(template_path), tmp_path, defaults=True, overwrite=True)
    assert not (tmp_path / "result.txt").exists()
    assert not (tmp_path / "extensions.py").exists()

"""Tests for the `extensions` module."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import copier
import pytest
from copier.errors import UserMessageError

TEMPLATES_DIRECTORY = Path(__file__).parent / "fixtures"


def git(*args: str | Path) -> None:
    """Run a git command.

    Arguments:
        *args: The git command to run.
    """
    subprocess.run(["git", *args], check=True)  # noqa: S603,S607


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
def test_extensions(tmp_path: Path, template_name: str, expected: str) -> None:
    """Test loader and context extensions.

    Arguments:
        tmp_path: A pytest fixture.
        template_name: The parametrized template to use.
        expected: The parametrized value we expect.
    """
    template_path = TEMPLATES_DIRECTORY / template_name
    copier.run_copy(str(template_path), tmp_path, defaults=True, overwrite=True, unsafe=True)
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
def test_extensions_raising_exceptions(tmp_path: Path, template_name: str, exception: type) -> None:
    """See what happens when an extension raises an exception.

    Arguments:
        tmp_path: A pytest fixture.
        template_name: The parametrized template to use.
        exception: The exception expected to be raised.
    """
    template_path = TEMPLATES_DIRECTORY / template_name
    with pytest.raises(exception):
        copier.run_copy(str(template_path), tmp_path, defaults=True, overwrite=True, unsafe=True)
    assert not (tmp_path / "result.txt").exists()
    assert not (tmp_path / "extensions.py").exists()


@pytest.mark.parametrize(
    "template_name",
    ["deprecation_warning_hook_return", "deprecation_warning_update_attr"],
)
def test_deprecated_usage(tmp_path: Path, template_name: str) -> None:
    """Test deprecation warnings.

    Arguments:
        tmp_path: A pytest fixture.
        template_name: The parametrized template to use.
    """
    template_path = TEMPLATES_DIRECTORY / template_name
    with pytest.warns(DeprecationWarning):
        copier.run_copy(str(template_path), tmp_path, defaults=True, overwrite=True, unsafe=True)
    result_file = tmp_path / "result.txt"
    assert result_file.exists()
    assert result_file.read_text() == "Success variable: True"


def test_update(tmp_path_factory: pytest.TempPathFactory) -> None:
    """Test updating a project.

    Arguments:
        tmp_path: A pytest fixture.
        expected: The parametrized value we expect.
    """
    src_path = tmp_path_factory.mktemp("template")
    dest_path = tmp_path_factory.mktemp("project")

    shutil.copytree(TEMPLATES_DIRECTORY / "update_project", src_path, dirs_exist_ok=True)
    git("-C", src_path, "init")
    git("-C", src_path, "add", "-A", ".")
    git("-C", src_path, "commit", "-m", "Initial commit")
    git("-C", src_path, "tag", "0.1.0")

    copier.run_copy(
        str(src_path),
        dest_path,
        unsafe=True,
        overwrite=True,
        defaults=True,
        data={"the_question": "the_answer"},
    )
    git("-C", dest_path, "init")
    git("-C", dest_path, "add", "-A", ".")
    git("-C", dest_path, "commit", "-m", "Initial commit")
    git("-C", dest_path, "tag", "1.0.0")

    copier.run_update(dest_path, unsafe=True, overwrite=True)

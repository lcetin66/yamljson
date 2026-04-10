"""Tests for the CLI module."""

from __future__ import annotations

import io
import json
from pathlib import Path

from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from yamljson.cli import main


def test_main_shows_usage_for_missing_args(capsys: CaptureFixture[str]) -> None:
    """CLI should return non-zero and print usage when args are missing."""

    result = main([])
    output = capsys.readouterr().out

    assert result == 1
    assert "Usage:" in output


def test_main_fails_when_to_parameter_is_missing(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """CLI should show usage when --to is missing."""

    file_path = tmp_path / "data.json"
    file_path.write_text("{}", encoding="utf-8")

    result = main([str(file_path), "yaml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "Usage:" in output


def test_main_fails_when_input_file_is_missing(capsys: CaptureFixture[str]) -> None:
    """CLI should fail with a file-not-found message for invalid input path."""

    result = main(["missing.json", "--to", "yaml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "File not found: missing.json" in output


def test_main_fails_when_option_is_invalid(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """CLI should reject options other than --to."""

    file_path = tmp_path / "data.json"
    file_path.write_text("{}", encoding="utf-8")

    result = main([str(file_path), "--format", "yaml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "Invalid option." in output


def test_main_fails_when_target_is_invalid(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """CLI should reject unknown target formats."""

    file_path = tmp_path / "data.json"
    file_path.write_text("{}", encoding="utf-8")

    result = main([str(file_path), "--to", "xml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "Unknown target format" in output


def test_main_fails_when_stdin_target_is_invalid(capsys: CaptureFixture[str]) -> None:
    """CLI should reject unsupported targets in stdin mode."""

    result = main(["--to", "toml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "Unknown target format" in output


def test_main_converts_json_to_yaml(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """CLI should convert JSON to YAML and return zero on success."""

    file_path = tmp_path / "data.json"
    file_path.write_text('{"name": "Alice"}', encoding="utf-8")

    result = main([str(file_path), "--to", "yaml"])
    output = capsys.readouterr().out
    yaml_file = tmp_path / "data.yaml"

    assert result == 0
    assert yaml_file.exists()
    assert "Converted JSON -> YAML" in output


def test_main_converts_yaml_to_json(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """CLI should convert YAML to JSON and return zero on success."""

    file_path = tmp_path / "data.yaml"
    file_path.write_text("name: Alice\n", encoding="utf-8")

    result = main([str(file_path), "--to", "json"])
    output = capsys.readouterr().out
    json_file = tmp_path / "data.json"

    assert result == 0
    assert json_file.exists()
    assert "Converted YAML -> JSON" in output

    parsed = json.loads(json_file.read_text(encoding="utf-8"))
    assert parsed == {"name": "Alice"}


def test_main_shows_conversion_error_for_invalid_json(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """CLI should surface conversion errors in a readable format."""

    file_path = tmp_path / "broken.json"
    file_path.write_text('{"name": "Alice",}', encoding="utf-8")

    result = main([str(file_path), "--to", "yaml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "Conversion failed:" in output


def test_main_converts_json_stdin_to_yaml_stdout(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    """CLI should support stdin -> stdout conversion for JSON input."""

    monkeypatch.setattr("sys.stdin", io.StringIO('{"name": "Alice"}'))

    result = main(["--to", "yaml"])
    output = capsys.readouterr().out

    assert result == 0
    assert "name: Alice" in output


def test_main_converts_yaml_stdin_to_json_stdout(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    """CLI should support stdin -> stdout conversion for YAML input."""

    monkeypatch.setattr("sys.stdin", io.StringIO("name: Alice\n"))

    result = main(["--to", "json"])
    output = capsys.readouterr().out

    assert result == 0
    parsed = json.loads(output)
    assert parsed == {"name": "Alice"}


def test_main_fails_for_invalid_stdin_content(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    """CLI should fail cleanly when stdin content cannot be parsed."""

    monkeypatch.setattr("sys.stdin", io.StringIO('{"name": "Alice",}'))

    result = main(["--to", "yaml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "Conversion failed:" in output

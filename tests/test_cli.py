"""Tests for the CLI module."""

from __future__ import annotations

import json

from yamljson.cli import main


def test_main_shows_usage_for_missing_args(capsys):
    """CLI should return non-zero and print usage when args are missing."""

    result = main([])
    output = capsys.readouterr().out

    assert result == 1
    assert "Usage:" in output


def test_main_fails_when_input_file_is_missing(capsys):
    """CLI should fail with a file-not-found message for invalid input path."""

    result = main(["missing.json", "--to", "yaml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "File not found: missing.json" in output


def test_main_fails_when_option_is_invalid(tmp_path, capsys):
    """CLI should reject options other than --to."""

    file_path = tmp_path / "data.json"
    file_path.write_text("{}", encoding="utf-8")

    result = main([str(file_path), "--format", "yaml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "Invalid option." in output


def test_main_fails_when_target_is_invalid(tmp_path, capsys):
    """CLI should reject unknown target formats."""

    file_path = tmp_path / "data.json"
    file_path.write_text("{}", encoding="utf-8")

    result = main([str(file_path), "--to", "xml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "Unknown target format" in output


def test_main_converts_json_to_yaml(tmp_path, capsys):
    """CLI should convert JSON to YAML and return zero on success."""

    file_path = tmp_path / "data.json"
    file_path.write_text('{"name": "Alice"}', encoding="utf-8")

    result = main([str(file_path), "--to", "yaml"])
    output = capsys.readouterr().out
    yaml_file = tmp_path / "data.yaml"

    assert result == 0
    assert yaml_file.exists()
    assert "Converted JSON -> YAML" in output


def test_main_converts_yaml_to_json(tmp_path, capsys):
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


def test_main_shows_conversion_error_for_invalid_json(tmp_path, capsys):
    """CLI should surface conversion errors in a readable format."""

    file_path = tmp_path / "broken.json"
    file_path.write_text('{"name": "Alice",}', encoding="utf-8")

    result = main([str(file_path), "--to", "yaml"])
    output = capsys.readouterr().out

    assert result == 1
    assert "Conversion failed:" in output

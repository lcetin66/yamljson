"""
This module provides tests for the converter module.
"""

import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import yaml

from yamljson.converter import (
    ConversionError,
    json_string_to_yaml,
    json_to_yaml,
    yaml_string_to_json,
    yaml_to_json,
)


def test_json_to_yaml(tmp_path: Path) -> None:
    """
    Test JSON to YAML conversion.

    Args:
        tmp_path (pathlib.Path): Temporary directory path.
    """
    json_file = tmp_path / "test.json"
    yaml_file = tmp_path / "test.yaml"

    data = [{"id": 1, "name": "Alice"}]

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f)

    json_to_yaml(json_file, yaml_file)

    with open(yaml_file, "r", encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)

    assert yaml_data == data


def test_yaml_to_json(tmp_path: Path) -> None:
    """
    Test YAML to JSON conversion.

    Args:
        tmp_path (pathlib.Path): Temporary directory path.
    """
    yaml_file = tmp_path / "test.yaml"
    json_file = tmp_path / "test.json"

    data = [{"id": 1, "name": "Alice"}]

    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f)

    yaml_to_json(yaml_file, json_file)

    with open(json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    assert json_data == data


def test_json_to_yaml_invalid_json_raises_conversion_error(tmp_path: Path) -> None:
    """Invalid JSON should raise ConversionError with a helpful message."""

    json_file = tmp_path / "invalid.json"
    yaml_file = tmp_path / "out.yaml"
    json_file.write_text('{"name": "Alice",}', encoding="utf-8")

    with pytest.raises(ConversionError, match="Invalid JSON format"):
        json_to_yaml(json_file, yaml_file)


def test_yaml_to_json_invalid_yaml_raises_conversion_error(tmp_path: Path) -> None:
    """Invalid YAML should raise ConversionError with a helpful message."""

    yaml_file = tmp_path / "invalid.yaml"
    json_file = tmp_path / "out.json"
    yaml_file.write_text("key: [1, 2", encoding="utf-8")

    with pytest.raises(ConversionError, match="Invalid YAML format"):
        yaml_to_json(yaml_file, json_file)


def test_yaml_to_json_non_serializable_data_raises_conversion_error(
    tmp_path: Path,
) -> None:
    """YAML values that cannot be represented in JSON should fail cleanly."""

    yaml_file = tmp_path / "data.yaml"
    json_file = tmp_path / "out.json"
    yaml_file.write_text("myset: !!set {a: null, b: null}\n", encoding="utf-8")

    with pytest.raises(ConversionError, match="cannot be represented in JSON"):
        yaml_to_json(yaml_file, json_file)


def test_json_string_to_yaml() -> None:
    """JSON string input should be converted into YAML output text."""

    output = json_string_to_yaml('{"id": 1, "name": "Alice"}')

    assert "id: 1" in output
    assert "name: Alice" in output


def test_yaml_string_to_json() -> None:
    """YAML string input should be converted into JSON output text."""

    output = yaml_string_to_json("id: 1\nname: Alice\n")

    assert json.loads(output) == {"id": 1, "name": "Alice"}


def test_json_string_to_yaml_invalid_input_raises_conversion_error() -> None:
    """Invalid JSON string input should raise ConversionError."""

    with pytest.raises(ConversionError, match="Invalid JSON format in stdin"):
        json_string_to_yaml('{"id": 1,}')


def test_yaml_string_to_json_invalid_input_raises_conversion_error() -> None:
    """Invalid YAML string input should raise ConversionError."""

    with pytest.raises(ConversionError, match="Invalid YAML format in stdin"):
        yaml_string_to_json("id: [1, 2")


def test_json_to_yaml_handles_large_payload_with_mock() -> None:
    """Large JSON payloads should be passed to YAML serialization cleanly."""

    large_payload = [{"id": i, "name": f"user-{i}"} for i in range(5000)]
    mocked_open = mock_open(read_data='{"placeholder": true}')

    with (
        patch("yamljson.converter.open", mocked_open),
        patch("yamljson.converter.json.load", return_value=large_payload),
        patch("yamljson.converter.yaml.safe_dump") as mocked_dump,
    ):
        json_to_yaml("large.json", "large.yaml")

    mocked_open.assert_any_call("large.json", "r", encoding="utf-8")
    mocked_open.assert_any_call("large.yaml", "w", encoding="utf-8")
    dumped_data, dumped_file = mocked_dump.call_args.args[:2]
    assert dumped_data == large_payload
    assert dumped_file is mocked_open()

"""
This module provides tests for the converter module.
"""

import json

import pytest
import yaml

from yamljson.converter import ConversionError, json_to_yaml, yaml_to_json


def test_json_to_yaml(tmp_path):
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


def test_yaml_to_json(tmp_path):
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


def test_json_to_yaml_invalid_json_raises_conversion_error(tmp_path):
    """Invalid JSON should raise ConversionError with a helpful message."""

    json_file = tmp_path / "invalid.json"
    yaml_file = tmp_path / "out.yaml"
    json_file.write_text('{"name": "Alice",}', encoding="utf-8")

    with pytest.raises(ConversionError, match="Invalid JSON format"):
        json_to_yaml(json_file, yaml_file)


def test_yaml_to_json_invalid_yaml_raises_conversion_error(tmp_path):
    """Invalid YAML should raise ConversionError with a helpful message."""

    yaml_file = tmp_path / "invalid.yaml"
    json_file = tmp_path / "out.json"
    yaml_file.write_text("key: [1, 2", encoding="utf-8")

    with pytest.raises(ConversionError, match="Invalid YAML format"):
        yaml_to_json(yaml_file, json_file)


def test_yaml_to_json_non_serializable_data_raises_conversion_error(tmp_path):
    """YAML values that cannot be represented in JSON should fail cleanly."""

    yaml_file = tmp_path / "data.yaml"
    json_file = tmp_path / "out.json"
    yaml_file.write_text("myset: !!set {a: null, b: null}\n", encoding="utf-8")

    with pytest.raises(ConversionError, match="cannot be represented in JSON"):
        yaml_to_json(yaml_file, json_file)

from __future__ import annotations

"""
This module provides the core functionality for converting files
between JSON and YAML formats.
"""

import json
from os import PathLike
from typing import Any, TypeAlias

import yaml

PathType: TypeAlias = str | PathLike[str]


class ConversionError(Exception):
    """Raised when an input/output conversion operation fails."""


def json_string_to_yaml(json_input: str) -> str:
    """Convert JSON string content to YAML string content."""

    try:
        data = json.loads(json_input)
    except json.JSONDecodeError as exc:
        raise ConversionError(
            "Invalid JSON format in stdin "
            f"(line {exc.lineno}, column {exc.colno})."
        ) from exc

    try:
        return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    except yaml.YAMLError as exc:
        raise ConversionError("Failed to serialize YAML output.") from exc


def yaml_string_to_json(yaml_input: str) -> str:
    """Convert YAML string content to JSON string content."""

    try:
        data = yaml.safe_load(yaml_input)
    except yaml.YAMLError as exc:
        raise ConversionError("Invalid YAML format in stdin.") from exc

    try:
        return json.dumps(data, indent=4)
    except TypeError as exc:
        raise ConversionError(
            "YAML content cannot be represented in JSON for stdout output."
        ) from exc


def json_to_yaml(json_file: PathType, yaml_file: PathType) -> None:
    """
    Convert JSON file to YAML file.

    Args:
        json_file (str): Path to the JSON file.
        yaml_file (str): Path to the YAML file.
    """
    try:
        with open(json_file, "r", encoding="utf-8") as jf:
            data: Any = json.load(jf)
    except FileNotFoundError as exc:
        raise ConversionError(f"Input file not found: {json_file}") from exc
    except PermissionError as exc:
        raise ConversionError(f"Permission denied while reading: {json_file}") from exc
    except json.JSONDecodeError as exc:
        raise ConversionError(
            "Invalid JSON format in "
            f"{json_file} (line {exc.lineno}, column {exc.colno})."
        ) from exc
    except OSError as exc:
        raise ConversionError(f"Failed to read input file: {exc}") from exc

    try:
        with open(yaml_file, "w", encoding="utf-8") as yf:
            yaml.safe_dump(data, yf, sort_keys=False, allow_unicode=True)
    except PermissionError as exc:
        raise ConversionError(
            f"Permission denied while writing output: {yaml_file}"
        ) from exc
    except OSError as exc:
        raise ConversionError(f"Failed to write output file: {exc}") from exc


def yaml_to_json(yaml_file: PathType, json_file: PathType) -> None:
    """
    Convert YAML file to JSON file.

    Args:
        yaml_file (str): Path to the YAML file.
        json_file (str): Path to the JSON file.
    """
    try:
        with open(yaml_file, "r", encoding="utf-8") as yf:
            data: Any = yaml.safe_load(yf)
    except FileNotFoundError as exc:
        raise ConversionError(f"Input file not found: {yaml_file}") from exc
    except PermissionError as exc:
        raise ConversionError(f"Permission denied while reading: {yaml_file}") from exc
    except yaml.YAMLError as exc:
        raise ConversionError(f"Invalid YAML format in {yaml_file}.") from exc
    except OSError as exc:
        raise ConversionError(f"Failed to read input file: {exc}") from exc

    try:
        with open(json_file, "w", encoding="utf-8") as jf:
            json.dump(data, jf, indent=4)
    except TypeError as exc:
        raise ConversionError(
            "YAML content cannot be represented in JSON "
            f"for output file {json_file}."
        ) from exc
    except PermissionError as exc:
        raise ConversionError(
            f"Permission denied while writing output: {json_file}"
        ) from exc
    except OSError as exc:
        raise ConversionError(f"Failed to write output file: {exc}") from exc

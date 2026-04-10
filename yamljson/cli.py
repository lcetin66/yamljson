"""
This module provides the CLI entry point for file conversion.
"""

import os
import sys

from .converter import ConversionError, json_to_yaml, yaml_to_json


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for file conversion."""

    args = sys.argv[1:] if argv is None else argv

    if len(args) != 3:
        print("Usage:")
        print("  convert <filename> --to yaml")
        print("  convert <filename> --to json")
        return 1

    filename, option, target = args

    if not os.path.isfile(filename):
        print(f"File not found: {filename}")
        return 1

    if option != "--to":
        print("Invalid option. Use: --to yaml | json")
        return 1

    base_name = filename.rsplit(".", 1)[0]

    if target not in {"yaml", "json"}:
        print("Unknown target format. Use 'yaml' or 'json'.")
        return 1

    try:
        if target == "yaml":
            yaml_file = f"{base_name}.yaml"
            json_to_yaml(filename, yaml_file)
            print(f"Converted JSON -> YAML: {yaml_file}")
        else:
            json_file = f"{base_name}.json"
            yaml_to_json(filename, json_file)
            print(f"Converted YAML -> JSON: {json_file}")
    except ConversionError as exc:
        print(f"Conversion failed: {exc}")
        return 1

    return 0

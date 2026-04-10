"""Top-level package for yamljson."""

from .converter import (
    ConversionError,
    json_string_to_yaml,
    json_to_yaml,
    yaml_string_to_json,
    yaml_to_json,
)

__all__: list[str] = [
    "ConversionError",
    "json_to_yaml",
    "yaml_to_json",
    "json_string_to_yaml",
    "yaml_string_to_json",
]
__version__ = "1.1.0"

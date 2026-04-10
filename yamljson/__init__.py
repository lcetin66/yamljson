"""Top-level package for yamljson."""

from .converter import ConversionError, json_to_yaml, yaml_to_json

__all__ = ["ConversionError", "json_to_yaml", "yaml_to_json"]
__version__ = "1.0.0"

# yamljson

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)
![CLI](https://img.shields.io/badge/interface-CLI-orange)
![Dependency](https://img.shields.io/badge/dependency-PyYAML-yellow)
![Format](https://img.shields.io/badge/conversion-JSON%20%E2%86%94%20YAML-informational)

A lightweight command-line tool to convert files between **JSON** and **YAML** formats.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Programmatic API](#programmatic-api)
- [Project Tree](#project-tree)
- [How It Works](#how-it-works)
- [Error Cases and Notes](#error-cases-and-notes)
- [Development](#development)

## Overview

`yamljson` is built for fast, simple, local file conversion:

- Convert `.json` files to `.yaml`
- Convert `.yaml` files to `.json`
- Use a single command with a predictable output filename

This project is ideal for quick data format switching in scripts, dev tooling, and config workflows.

## Features

- Simple CLI command: `convert`
- Bidirectional conversion: JSON to YAML, YAML to JSON
- UTF-8 file handling
- Human-readable JSON output (`indent=4`)
- Safe YAML operations (`yaml.safe_load`, `yaml.safe_dump`)

## Requirements

- Python `>=3.8`
- `PyYAML`

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd yamljson
```

### 2. Install locally

```bash
pip install .
```

This registers the CLI script:

```bash
convert
```

## Usage

### CLI syntax

```bash
convert <filename> --to yaml
convert <filename> --to json
```

### Examples

#### JSON to YAML

```bash
convert data.json --to yaml
```

Output file:

```text
data.yaml
```

#### YAML to JSON

```bash
convert config.yaml --to json
```

Output file:

```text
config.json
```

### Common CLI responses

- `File not found: <filename>` if the input file does not exist
- `Invalid option. Use: --to yaml | json` if `--to` is missing
- `Unknown target format. Use 'yaml' or 'json'.` for unsupported targets
- `Conversion failed: <reason>` for parsing and file I/O errors

## Programmatic API

You can also use the converter functions directly in Python:

```python
from yamljson.converter import ConversionError, json_to_yaml, yaml_to_json

try:
    json_to_yaml("data.json", "data.yaml")
    yaml_to_json("config.yaml", "config.json")
except ConversionError as exc:
    print(f"Conversion failed: {exc}")
```

## Project Tree

```text
yamljson/
├── LICENSE
├── README.md
├── pyproject.toml
├── tests/
│   ├── test_cli.py
│   └── test_converter.py
└── yamljson/
    ├── __init__.py
    ├── cli.py
    └── converter.py
```

## How It Works

1. `yamljson/cli.py` parses CLI arguments.
2. It validates the file path and conversion target.
3. It routes the operation to:
   - `json_to_yaml(...)` or
   - `yaml_to_json(...)`
4. `yamljson/converter.py` reads input and writes converted output.

## Error Cases and Notes

- Invalid JSON input raises `ConversionError`.
- Invalid YAML input raises `ConversionError`.
- YAML values not representable in JSON raise `ConversionError`.
- Output files are created in the same directory as the input file.
- Output filename is generated from the input basename:
  - `name.json` -> `name.yaml`
  - `name.yaml` -> `name.json`

## Development

Install editable mode for local development:

```bash
pip install -e .
```

Run tests (if/when tests are added/expanded):

```bash
python -m pytest
```

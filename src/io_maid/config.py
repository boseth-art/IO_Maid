"""Configuration loading and merging for IO_Maid."""

import json
from pathlib import Path


def get_default_config_path() -> Path:
    """Return the path to the bundled default config file."""
    return Path(__file__).resolve().parent.parent.parent / "config" / "default_config.json"


def load_config(config_path: Path | None = None) -> dict:
    """Load config from a JSON file, falling back to defaults.

    If config_path is provided, loads that file and merges with defaults.
    Otherwise loads the bundled default config.
    """
    default = _load_json(get_default_config_path())

    if config_path is None:
        return default

    override = _load_json(config_path)
    return merge_configs(default, override)


def merge_configs(default: dict, override: dict) -> dict:
    """Deep-merge override into default. Override wins for top-level keys.

    For lists (like categories), the override replaces the entire list.
    """
    result = default.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result


def _load_json(path: Path) -> dict:
    """Load and return a JSON file as a dict."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)

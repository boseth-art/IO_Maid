"""Tests for config loading and merging."""

import json
import pytest
from pathlib import Path

from io_maid.config import load_config, merge_configs, get_default_config_path


class TestLoadConfig:
    def test_default_config_has_required_keys(self):
        config = load_config()
        assert "download_dir" in config
        assert "categories" in config
        assert "skip_names" in config
        assert "skip_dirs" in config

    def test_default_config_has_categories(self):
        config = load_config()
        assert len(config["categories"]) == 11
        folders = [c["folder"] for c in config["categories"]]
        assert "_WhatsApp" in folders
        assert "_Images" in folders
        assert "_Documents" in folders

    def test_load_custom_config(self, tmp_path):
        custom = {"download_dir": "/tmp/test", "skip_names": ["custom.txt"]}
        custom_file = tmp_path / "config.json"
        custom_file.write_text(json.dumps(custom))

        config = load_config(custom_file)
        assert config["download_dir"] == "/tmp/test"
        assert "custom.txt" in config["skip_names"]

    def test_default_config_path_exists(self):
        assert get_default_config_path().exists()


class TestMergeConfigs:
    def test_override_replaces_top_level(self):
        default = {"a": 1, "b": 2}
        override = {"b": 3}
        result = merge_configs(default, override)
        assert result == {"a": 1, "b": 3}

    def test_override_adds_new_keys(self):
        default = {"a": 1}
        override = {"b": 2}
        result = merge_configs(default, override)
        assert result == {"a": 1, "b": 2}

    def test_override_replaces_lists(self):
        default = {"items": [1, 2, 3]}
        override = {"items": [4, 5]}
        result = merge_configs(default, override)
        assert result["items"] == [4, 5]

    def test_deep_merge_dicts(self):
        default = {"nested": {"x": 1, "y": 2}}
        override = {"nested": {"y": 3, "z": 4}}
        result = merge_configs(default, override)
        assert result["nested"] == {"x": 1, "y": 3, "z": 4}

    def test_empty_override_returns_default(self):
        default = {"a": 1, "b": 2}
        result = merge_configs(default, {})
        assert result == {"a": 1, "b": 2}

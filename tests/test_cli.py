"""Tests for CLI argument parsing."""

import pytest
from pathlib import Path
from unittest.mock import patch

from io_maid.cli import main


class TestCLIParsing:
    def test_no_args_uses_defaults(self):
        """With no args, should use default config."""
        with patch("io_maid.cli.load_config") as mock_load:
            with patch("io_maid.cli.organize") as mock_organize:
                mock_organize.return_value = {"moved": 0, "skipped": 0, "errors": []}
                with patch("sys.argv", ["io-maid"]):
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    assert exc_info.value.code == 0
                mock_load.assert_called_once_with(None)

    def test_dir_flag(self, tmp_path):
        """--dir should override download_dir in config."""
        with patch("io_maid.cli.load_config") as mock_load:
            with patch("io_maid.cli.organize") as mock_organize:
                mock_load.return_value = {"download_dir": "~/Downloads"}
                mock_organize.return_value = {"moved": 0, "skipped": 0, "errors": []}
                with patch("sys.argv", ["io-maid", "--dir", str(tmp_path)]):
                    with pytest.raises(SystemExit):
                        main()
                call_config = mock_organize.call_args[0][0]
                assert call_config["download_dir"] == str(tmp_path)

    def test_dry_run_flag(self):
        """--dry-run should pass dry_run=True."""
        with patch("io_maid.cli.load_config") as mock_load:
            with patch("io_maid.cli.organize") as mock_organize:
                mock_load.return_value = {"download_dir": "/tmp"}
                mock_organize.return_value = {"moved": 0, "skipped": 0, "errors": []}
                with patch("sys.argv", ["io-maid", "--dry-run"]):
                    with pytest.raises(SystemExit):
                        main()
                assert mock_organize.call_args[1]["dry_run"] is True

    def test_verbose_flag(self):
        """--verbose should pass verbose=True."""
        with patch("io_maid.cli.load_config") as mock_load:
            with patch("io_maid.cli.organize") as mock_organize:
                mock_load.return_value = {"download_dir": "/tmp"}
                mock_organize.return_value = {"moved": 0, "skipped": 0, "errors": []}
                with patch("sys.argv", ["io-maid", "--verbose"]):
                    with pytest.raises(SystemExit):
                        main()
                assert mock_organize.call_args[1]["verbose"] is True

    def test_config_flag(self, tmp_path):
        """--config should load custom config file."""
        with patch("io_maid.cli.load_config") as mock_load:
            with patch("io_maid.cli.organize") as mock_organize:
                mock_load.return_value = {"download_dir": "/tmp"}
                mock_organize.return_value = {"moved": 0, "skipped": 0, "errors": []}
                config_file = tmp_path / "custom.json"
                with patch("sys.argv", ["io-maid", "--config", str(config_file)]):
                    with pytest.raises(SystemExit):
                        main()
                mock_load.assert_called_once_with(config_file)

    def test_exit_code_on_errors(self):
        """Should exit with code 1 when errors occur."""
        with patch("io_maid.cli.load_config") as mock_load:
            with patch("io_maid.cli.organize") as mock_organize:
                mock_load.return_value = {"download_dir": "/tmp"}
                mock_organize.return_value = {"moved": 0, "skipped": 0, "errors": ["file.txt"]}
                with patch("sys.argv", ["io-maid"]):
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    assert exc_info.value.code == 1

    def test_exit_code_clean(self):
        """Should exit with code 0 when no errors."""
        with patch("io_maid.cli.load_config") as mock_load:
            with patch("io_maid.cli.organize") as mock_organize:
                mock_load.return_value = {"download_dir": "/tmp"}
                mock_organize.return_value = {"moved": 5, "skipped": 2, "errors": []}
                with patch("sys.argv", ["io-maid"]):
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    assert exc_info.value.code == 0

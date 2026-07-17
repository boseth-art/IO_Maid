"""Integration tests for the full organize() loop."""

import pytest
from pathlib import Path

from io_maid.organizer import organize
from io_maid.config import load_config


@pytest.fixture
def config(tmp_path):
    """Config pointing to a temporary downloads directory."""
    cfg = load_config()
    cfg["download_dir"] = str(tmp_path)
    return cfg


@pytest.fixture
def downloads_dir(config):
    """The temporary downloads directory."""
    return Path(config["download_dir"])


class TestOrganizeIntegration:
    def test_classifies_all_types(self, downloads_dir, config):
        """Create representative files and verify they end up in correct folders."""
        files = {
            "photo.jpg": "_Images",
            "icon.png": "_Images",
            "resume.docx": "_Documents",
            "paper.pdf": "_Academic_Papers",
            "archive.zip": "_Archives",
            "data.csv": "_Data",
            "notes.txt": "_Text",
            "app.dmg": "_Installers",
            "WhatsApp Image 2024.jpg": "_WhatsApp",
            "Screen Shot 2024.png": "_Screenshots",
            "design.drawio": "_Diagrams",
        }

        for fname in files:
            (downloads_dir / fname).write_text("test content")

        result = organize(config)

        assert result["errors"] == []
        assert result["moved"] == len(files)

        for fname, expected_folder in files.items():
            target = downloads_dir / expected_folder / fname
            assert target.exists(), f"{fname} should be in {expected_folder}"

    def test_idempotent(self, downloads_dir, config):
        """Running organize twice should move nothing on the second run."""
        (downloads_dir / "photo.jpg").write_text("test")

        result1 = organize(config)
        assert result1["moved"] == 1

        result2 = organize(config)
        assert result2["moved"] == 0

    def test_skips_already_organized(self, downloads_dir, config):
        """Files already in their target folder should be skipped."""
        target_dir = downloads_dir / "_Images"
        target_dir.mkdir()
        (target_dir / "photo.jpg").write_text("test")

        result = organize(config)
        assert result["moved"] == 0
        assert (target_dir / "photo.jpg").exists()

    def test_skips_system_files(self, downloads_dir, config):
        """System files should be skipped."""
        (downloads_dir / ".DS_Store").write_text("skip")
        (downloads_dir / ".localized").write_text("skip")

        result = organize(config)
        assert result["moved"] == 0

    def test_app_bundle_moved(self, downloads_dir, config):
        """App bundles (directories ending in .app) should be moved."""
        app_dir = downloads_dir / "MyApp.app"
        app_dir.mkdir()
        (app_dir / "Contents").mkdir()

        result = organize(config)
        assert result["moved"] == 1
        assert (downloads_dir / "_Applications" / "MyApp.app").exists()

    def test_dry_run_no_moves(self, downloads_dir, config):
        """Dry run should not move any files."""
        (downloads_dir / "photo.jpg").write_text("test")
        (downloads_dir / "data.csv").write_text("test")

        result = organize(config, dry_run=True)
        assert result["moved"] == 2
        assert (downloads_dir / "photo.jpg").exists()
        assert (downloads_dir / "data.csv").exists()
        assert not (downloads_dir / "_Images").exists()

    def test_unclassified_files_skipped(self, downloads_dir, config):
        """Files with no matching category should be skipped."""
        (downloads_dir / "unknown.xyz").write_text("test")

        result = organize(config)
        assert result["skipped"] >= 1
        assert (downloads_dir / "unknown.xyz").exists()

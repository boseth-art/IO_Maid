"""Tests for file classification logic."""

import pytest
from pathlib import Path

from io_maid.classifier import classify
from io_maid.config import load_config


@pytest.fixture
def config():
    return load_config()


class TestSkipConditions:
    def test_ds_store_skipped(self, config):
        item = Path("/fake/.DS_Store")
        assert classify(item, config) is None

    def test_localized_skipped(self, config):
        item = Path("/fake/.localized")
        assert classify(item, config) is None

    def test_dotfiles_skipped(self, config):
        item = Path("/fake/.hidden_file.xyz")
        assert classify(item, config) is None

    def test_dotfile_with_allowed_ext(self, config):
        item = Path("/fake/.notes.txt")
        assert classify(item, config) == "_Text"

    def test_macos_resource_fork_skipped(self, config):
        item = Path("/fake/._myfile.pdf")
        assert classify(item, config) is None

    def test_organizer_log_skipped(self, config):
        item = Path("/fake/_organizer.log")
        assert classify(item, config) is None


class TestCategoryClassification:
    def test_app_bundle(self, config, tmp_path):
        app_dir = tmp_path / "MyApp.app"
        app_dir.mkdir()
        assert classify(app_dir, config) == "_Applications"

    def test_whatsapp_image(self, config):
        item = Path("/fake/WhatsApp Image 2024-01-01 at 10.30.00.jpeg")
        assert classify(item, config) == "_WhatsApp"

    def test_whatsapp_video(self, config):
        item = Path("/fake/WhatsApp Video 2024-01-01.mp4")
        assert classify(item, config) == "_WhatsApp"

    def test_screenshot(self, config):
        item = Path("/fake/Screen Shot 2024-01-01 at 10.30.00.png")
        assert classify(item, config) == "_Screenshots"

    def test_untitled_diagram(self, config):
        item = Path("/fake/Untitled diagram.png")
        assert classify(item, config) == "_Screenshots"

    def test_wallhaven(self, config):
        item = Path("/fake/wallhaven-abc123.jpg")
        assert classify(item, config) == "_Screenshots"

    def test_drawio(self, config):
        item = Path("/fake/presentation.drawio")
        assert classify(item, config) == "_Diagrams"

    def test_drawio_bkp(self, config):
        item = Path("/fake/income management system.drawio.bkp")
        assert classify(item, config) == "_Diagrams"

    def test_page_export(self, config):
        item = Path("/fake/diagram_page-0001.jpg")
        assert classify(item, config) == "_Diagrams"

    def test_dmg_installer(self, config):
        item = Path("/fake/AppInstaller.dmg")
        assert classify(item, config) == "_Installers"

    def test_zip_archive(self, config):
        item = Path("/fake/archive.zip")
        assert classify(item, config) == "_Archives"

    def test_tar_gz_archive(self, config):
        item = Path("/fake/source.tar.gz")
        assert classify(item, config) == "_Archives"

    def test_rar_archive(self, config):
        item = Path("/fake/files.rar")
        assert classify(item, config) == "_Archives"

    def test_pdf(self, config):
        item = Path("/fake/paper.pdf")
        assert classify(item, config) == "_Academic_Papers"

    def test_docx(self, config):
        item = Path("/fake/resume.docx")
        assert classify(item, config) == "_Documents"

    def test_jpg_image(self, config):
        item = Path("/fake/photo.jpg")
        assert classify(item, config) == "_Images"

    def test_png_image(self, config):
        item = Path("/fake/screenshot.png")
        assert classify(item, config) == "_Images"

    def test_svg_image(self, config):
        item = Path("/fake/icon.svg")
        assert classify(item, config) == "_Images"

    def test_json_data(self, config):
        item = Path("/fake/data.json")
        assert classify(item, config) == "_Data"

    def test_csv_data(self, config):
        item = Path("/fake/spreadsheet.csv")
        assert classify(item, config) == "_Data"

    def test_python_data(self, config):
        item = Path("/fake/script.py")
        assert classify(item, config) == "_Data"

    def test_yaml_data(self, config):
        item = Path("/fake/config.yaml")
        assert classify(item, config) == "_Data"

    def test_txt(self, config):
        item = Path("/fake/notes.txt")
        assert classify(item, config) == "_Text"

    def test_unclassified(self, config):
        item = Path("/fake/unknown.xyz")
        assert classify(item, config) is None


class TestPriorityOrdering:
    def test_whatsapp_before_general_image(self, config):
        """WhatsApp images should be classified as _WhatsApp, not _Images."""
        item = Path("/fake/WhatsApp Image 2024.jpg")
        assert classify(item, config) == "_WhatsApp"

    def test_screenshot_before_general_image(self, config):
        """Screenshots should be classified as _Screenshots, not _Images."""
        item = Path("/fake/Screen Shot 2024.png")
        assert classify(item, config) == "_Screenshots"

    def test_drawio_page_before_general_image(self, config):
        """Drawio page exports should be _Diagrams, not _Images."""
        item = Path("/fake/mydiagram_page-0001.jpg")
        assert classify(item, config) == "_Diagrams"

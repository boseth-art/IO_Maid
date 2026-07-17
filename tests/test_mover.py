"""Tests for file moving with dedup and collision handling."""

import pytest
from pathlib import Path

from io_maid.mover import safe_move


class TestSafeMove:
    def test_basic_move(self, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        dst_dir = tmp_path / "dest"

        result = safe_move(src, dst_dir)
        assert result.exists()
        assert result == dst_dir / "file.txt"
        assert not src.exists()

    def test_dedup_same_size(self, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()
        existing = dst_dir / "file.txt"
        existing.write_text("hello")

        result = safe_move(src, dst_dir)
        assert result.exists()
        assert result.read_text() == "hello"
        assert not src.exists()

    def test_dedup_dir(self, tmp_path):
        src = tmp_path / "mydir"
        src.mkdir()
        (src / "child.txt").write_text("data")
        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()
        existing = dst_dir / "mydir"
        existing.mkdir()

        result = safe_move(src, dst_dir)
        assert result.exists()
        assert not src.exists()

    def test_name_collision(self, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("new content with different size")
        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()
        existing = dst_dir / "file.txt"
        existing.write_text("old")

        result = safe_move(src, dst_dir)
        assert result.exists()
        assert result.name == "file (1).txt"
        assert result.read_text() == "new content with different size"
        assert existing.read_text() == "old"

    def test_multiple_collisions(self, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("third with unique content here")
        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()
        (dst_dir / "file.txt").write_text("first")
        (dst_dir / "file (1).txt").write_text("second")

        result = safe_move(src, dst_dir)
        assert result.name == "file (2).txt"

    def test_creates_destination_dir(self, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        dst_dir = tmp_path / "new" / "nested" / "dest"

        result = safe_move(src, dst_dir)
        assert dst_dir.exists()
        assert result.exists()

    def test_dry_run_no_move(self, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        dst_dir = tmp_path / "dest"

        result = safe_move(src, dst_dir, dry_run=True)
        assert src.exists()
        assert not dst_dir.exists()
        assert result == dst_dir / "file.txt"

    def test_dry_run_no_dedup(self, tmp_path):
        src = tmp_path / "file.txt"
        src.write_text("hello")
        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()
        (dst_dir / "file.txt").write_text("hello")

        result = safe_move(src, dst_dir, dry_run=True)
        assert src.exists()
        assert result == dst_dir / "file.txt"

"""File moving with deduplication and collision handling for IO_Maid."""

import logging
import shutil
from pathlib import Path


def safe_move(src: Path, dst_dir: Path, *, dry_run: bool = False) -> Path:
    """Move src into dst_dir, handling name collisions and dedup.

    - If a file with the same name and size exists, the source is deleted (dedup).
    - If a file with the same name but different size exists, appends (1), (2), etc.
    - If dry_run is True, logs intended actions without actually moving files.

    Returns the final destination path.
    """
    if not dry_run:
        dst_dir.mkdir(parents=True, exist_ok=True)

    dst = dst_dir / src.name

    # Dedup: same name + same size
    if dst.exists() and src.exists() and src.stat().st_size == dst.stat().st_size:
        if dry_run:
            logging.info(f"  [DRY RUN] Would dedup (size match): {src.name}")
        else:
            if src.is_dir():
                shutil.rmtree(src)
            else:
                src.unlink()
            logging.info(f"  Deduped (size match): {src.name}")
        return dst

    # Name collision: append (1), (2), etc.
    if dst.exists():
        stem = src.stem
        suffix = src.suffix
        counter = 1
        while dst.exists():
            dst = dst_dir / f"{stem} ({counter}){suffix}"
            counter += 1

    if dry_run:
        logging.info(f"  [DRY RUN] Would move: {src.name} -> {dst_dir.name}/{dst.name}")
    else:
        shutil.move(str(src), str(dst))
        logging.info(f"  Moved: {src.name} -> {dst_dir.name}/{dst.name}")

    return dst

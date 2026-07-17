"""Main orchestration loop for IO_Maid."""

import logging
import sys
from pathlib import Path

from io_maid.classifier import classify
from io_maid.mover import safe_move


def organize(config: dict, *, dry_run: bool = False, verbose: bool = False) -> dict:
    """Run the full organize loop on the configured directory.

    Returns a summary dict: {"moved": int, "skipped": int, "errors": list[str]}
    """
    _setup_logging(verbose)

    download_dir = Path(config["download_dir"]).expanduser()
    log_file = config.get("log_file", "_organizer.log")
    skip_dirs = set(config.get("skip_dirs", []))
    skip_names = set(config.get("skip_names", []))

    logging.info("=== IO_Maid organize run ===")

    moved_count = 0
    skipped_count = 0
    errors: list[str] = []

    entries = sorted(download_dir.iterdir())
    for item in entries:
        # Skip directories (except .app bundles)
        if item.is_dir():
            if item.name in skip_dirs or item.name.startswith("."):
                continue
            if item.name.endswith(".app"):
                try:
                    safe_move(item, download_dir / "_Applications", dry_run=dry_run)
                    moved_count += 1
                except Exception as e:
                    logging.error(f"  Error moving {item.name}: {e}")
                    errors.append(item.name)
                continue
            continue

        # Skip system/skip files
        if item.name in skip_names or item.name.startswith("._"):
            continue

        folder = classify(item, config)
        if folder is None:
            logging.info(f"  Skipped (unclassified): {item.name}")
            skipped_count += 1
            continue

        dest_dir = download_dir / folder
        # Already inside its target folder
        if dest_dir == item.parent:
            skipped_count += 1
            continue

        try:
            safe_move(item, dest_dir, dry_run=dry_run)
            moved_count += 1
        except Exception as e:
            logging.error(f"  Error moving {item.name}: {e}")
            errors.append(item.name)

    logging.info(f"Done: {moved_count} moved, {skipped_count} skipped, {len(errors)} errors")
    if errors:
        logging.warning(f"Errors: {errors}")

    return {"moved": moved_count, "skipped": skipped_count, "errors": errors}


def _setup_logging(verbose: bool) -> None:
    """Configure logging to stdout (if verbose) and file."""
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]

    if not verbose:
        # Suppress console output unless verbose
        handlers[0].setLevel(logging.WARNING)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers,
        force=True,
    )

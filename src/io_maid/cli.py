"""CLI interface for IO_Maid with launchd auto-organize support."""

import argparse
import subprocess
import sys
from pathlib import Path

from io_maid.config import load_config
from io_maid.organizer import organize

PLIST_LABEL = "com.io-maid.watch"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{PLIST_LABEL}.plist"


def main():
    parser = argparse.ArgumentParser(
        prog="io-maid",
        description="IO_Maid — Auto-organize your Downloads folder",
    )
    parser.add_argument("--dir", "-d", type=Path,
                        help="Directory to organize (default: ~/Downloads)")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="Show what would be done without moving files")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print detailed output to console")
    parser.add_argument("--config", "-c", type=Path,
                        help="Path to custom config JSON file")
    parser.add_argument("--install", action="store_true",
                        help="Install macOS launchd agent for auto-organize")
    parser.add_argument("--uninstall", action="store_true",
                        help="Remove the launchd auto-organize agent")
    parser.add_argument("--status", action="store_true",
                        help="Check if the launchd agent is active")

    args = parser.parse_args()

    if args.install:
        _install_launchd()
        return

    if args.uninstall:
        _uninstall_launchd()
        return

    if args.status:
        _check_status()
        return

    # Load and merge config
    config = load_config(args.config)
    if args.dir:
        config["download_dir"] = str(args.dir)

    # Run organizer
    result = organize(config, dry_run=args.dry_run, verbose=args.verbose)

    sys.exit(1 if result["errors"] else 0)


def _install_launchd() -> None:
    """Generate and install the launchd plist for auto-organize."""
    io_maid_path = _find_io_maid_path()

    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_LABEL}</string>
    <key>WatchPaths</key>
    <array>
        <string>{Path.home() / "Downloads"}</string>
    </array>
    <key>ThrottleInterval</key>
    <integer>5</integer>
    <key>ProgramArguments</key>
    <array>
        <string>{io_maid_path}</string>
        <string>--verbose</string>
    </array>
    <key>StandardOutPath</key>
    <string>/tmp/io-maid.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/io-maid-error.log</string>
</dict>
</plist>"""

    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLIST_PATH.write_text(plist_content)
    print(f"Plist installed: {PLIST_PATH}")

    # Load the agent
    result = subprocess.run(
        ["launchctl", "load", str(PLIST_PATH)],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print("Auto-organize agent loaded. IO_Maid will now organize files automatically.")
    else:
        print(f"Warning: launchctl load returned: {result.stderr.strip()}")


def _uninstall_launchd() -> None:
    """Remove the launchd plist."""
    if not PLIST_PATH.exists():
        print("No launchd agent found. Nothing to uninstall.")
        return

    subprocess.run(
        ["launchctl", "unload", str(PLIST_PATH)],
        capture_output=True, text=True,
    )
    PLIST_PATH.unlink()
    print("Auto-organize agent removed.")


def _check_status() -> None:
    """Check if the launchd agent is loaded."""
    result = subprocess.run(
        ["launchctl", "list"],
        capture_output=True, text=True,
    )
    if PLIST_LABEL in result.stdout:
        print(f"IO_Maid auto-organize agent is ACTIVE (loaded).")
        print(f"Plist: {PLIST_PATH}")
    else:
        print(f"IO_Maid auto-organize agent is NOT active.")
        print(f"Run 'io-maid --install' to enable auto-organize.")


def _find_io_maid_path() -> str:
    """Find the io-maid executable path."""
    import shutil
    path = shutil.which("io-maid")
    if path:
        return path
    # Fallback: use python -m
    return f"{sys.executable} -m io_maid"

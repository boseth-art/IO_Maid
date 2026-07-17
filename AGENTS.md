# AGENTS.md

## Project

IO_Maid — macOS CLI that auto-organizes `~/Downloads` into category folders by file type/name. Single-package Python project, no runtime dependencies.

## Commands

```bash
# Setup (virtual env required — pip is externally managed on macOS)
cd ~/personal\ project/IO_Maid
source .venv/bin/activate
pip install -e ".[dev]"

# Run
io-maid                    # Organize ~/Downloads
io-maid --dry-run          # Preview without moving
io-maid --verbose          # Show details
io-maid --dir ~/Desktop    # Organize different folder
io-maid --install          # Enable launchd auto-organize
io-maid --uninstall        # Disable auto-organize
io-maid --status           # Check auto-organize state

# Tests
pytest -v                  # Run all 64 tests
pytest tests/test_classifier.py -v   # Run single test file
```

## Architecture

```
src/io_maid/
  cli.py          → argparse entry point, launchd install/uninstall
  config.py       → loads JSON config, merges user overrides
  classifier.py   → rule-based file classification (first match wins)
  mover.py        → safe_move with dedup (size match) + collision handling
  organizer.py    → main loop: classify → move
config/default_config.json → 11 category rules, skip lists
```

## Key Conventions

- **src/ layout**: package is `src/io_maid/`, not root-level
- **Zero dependencies**: only stdlib + pytest for dev
- **JSON config**: categories are declarative in `config/default_config.json`, not hardcoded in Python
- **Condition types**: `ext_equals`, `ext_in`, `name_contains`, `name_contains_lower`, `name_startswith`, `dir_name_endswith`
- **Priority order**: categories array order determines which rule wins (first match)
- **Auto-organize**: uses macOS launchd `WatchPaths` — no background daemon, triggered by folder changes

## Gotchas

- macOS `pip` is externally managed — always use the `.venv`
- `name_contains` condition supports both `"value"` (string) and `"values"` (list)
- Files starting with `._` are macOS resource forks — always skipped
- Dedup is size-only (no checksum) — same-size files with different content get deduped
- The `log_file` config key exists but logging currently goes to stdout only (not implemented in organizer.py)

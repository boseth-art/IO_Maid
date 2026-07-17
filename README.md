<p align="center">
  <img src="logo.jpg" alt="IO_Maid Logo" width="200"/>
</p>

<h1 align="center">IO_Maid</h1>

<p align="center">
  Auto-organize your Downloads folder by file type and name patterns
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#platform-support">Platforms</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#category-rules">Rules</a> •
  <a href="#running-tests">Tests</a>
</p>

---

## What is IO_Maid?

IO_Maid watches your Downloads folder and automatically sorts files into organized subfolders based on their type. New downloads are organized within seconds — no manual intervention needed.

### Before & After

```
BEFORE: ~/Downloads/
├── photo.jpg
├── resume.docx
├── paper.pdf
├── archive.zip
├── data.csv
├── WhatsApp Image 2024.jpg
├── Screen Shot 2024.png
├── installer.dmg
├── notes.txt
└── design.drawio

AFTER: ~/Downloads/
├── _Academic_Papers/
│   └── paper.pdf
├── _Archives/
│   └── archive.zip
├── _Data/
│   └── data.csv
├── _Diagrams/
│   └── design.drawio
├── _Documents/
│   └── resume.docx
├── _Images/
│   └── photo.jpg
├── _Installers/
│   └── installer.dmg
├── _Screenshots/
│   └── Screen Shot 2024.png
├── _Text/
│   └── notes.txt
└── _WhatsApp/
    └── WhatsApp Image 2024.jpg
```

## Ownership

| | |
|---|---|
| **Author** | Boseth Rathnayake |
| **GitHub** | [github.com/boseth-art/IO_Maid](https://github.com/boseth-art/IO_Maid) |
| **License** | MIT |
| **Version** | 1.0.0 |
| **Python** | >= 3.10 |

## Platform Support

IO_Maid works on **macOS**, **Windows**, and **Linux**.

### macOS (Full Support)

| Feature | Status |
|---|---|
| Manual organize | Supported |
| Auto-organize (launchd) | Supported |
| Dry-run mode | Supported |
| Custom config | Supported |
| Apple Silicon (M1/M2/M3/M4) | Supported |
| Intel Macs | Supported |

**Supported macOS versions:** Ventura (13), Sonoma (14), Sequoia (15), Monterey (12), Big Sur (11), Catalina (10.15)

### Windows (Full Support)

| Feature | Status |
|---|---|
| Manual organize | Supported |
| Auto-organize (Task Scheduler) | Supported |
| Dry-run mode | Supported |
| Custom config | Supported |
| Windows 10/11 | Supported |

**Supported Windows versions:** Windows 10, Windows 11

### Linux (Full Support)

| Feature | Status |
|---|---|
| Manual organize | Supported |
| Auto-organize (cron) | Supported |
| Dry-run mode | Supported |
| Custom config | Supported |
| Ubuntu, Fedora, Arch | Supported |

## Installation

### Option 1: Install from GitHub (all platforms)

```bash
pip install git+https://github.com/boseth-art/IO_Maid.git
```

### Option 2: Clone and install locally

```bash
git clone https://github.com/boseth-art/IO_Maid.git
cd IO_Maid
pip install -e ".[dev]"
```

### Option 3: Manual setup

```bash
# Clone the repository
git clone https://github.com/boseth-art/IO_Maid.git
cd IO_Maid

# Create a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install in development mode
pip install -e ".[dev]"
```

After installation, the `io-maid` command is available globally.

## Usage

### Manual organize

```bash
# Organize ~/Downloads (default)
io-maid

# Preview what would happen (no files moved)
io-maid --dry-run

# Verbose output
io-maid --verbose

# Organize a different directory
io-maid --dir ~/Desktop

# Use a custom config file
io-maid --config ~/my-config.json
```

### Example terminal session

```bash
$ io-maid --dry-run --verbose
2024-01-15 10:30:01 [INFO] === IO_Maid organize run ===
2024-01-15 10:30:01 [INFO]   [DRY RUN] Would move: photo.jpg -> _Images/
2024-01-15 10:30:01 [INFO]   [DRY RUN] Would move: resume.docx -> _Documents/
2024-01-15 10:30:01 [INFO]   [DRY RUN] Would move: paper.pdf -> _Academic_Papers/
2024-01-15 10:30:01 [INFO]   [DRY RUN] Would move: archive.zip -> _Archives/
2024-01-15 10:30:01 [INFO]   Skipped (unclassified): unknown.xyz
2024-01-15 10:30:01 [INFO] Done: 4 moved, 1 skipped, 0 errors
```

### Auto-organize

Enable automatic organization whenever new files are downloaded:

#### macOS (launchd)
```bash
io-maid --install      # Install the launchd agent
io-maid --status       # Check if it's active
io-maid --uninstall    # Disable auto-organize
```

#### Windows (Task Scheduler)
```bash
io-maid --install      # Install the scheduled task
io-maid --status       # Check if it's active
io-maid --uninstall    # Disable auto-organize
```

#### Linux (cron)
```bash
io-maid --install      # Install the cron job
io-maid --status       # Check if it's active
io-maid --uninstall    # Disable auto-organize
```

## How It Works

### Auto-Organize Architecture

IO_Maid uses the native task scheduler of each operating system:

| Platform | Service | Trigger |
|---|---|---|
| **macOS** | launchd + WatchPaths | Filesystem change |
| **Windows** | Task Scheduler | Every 5 minutes |
| **Linux** | cron | Every 5 minutes |

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Downloads   │────▶│  OS Task     │────▶│  IO_Maid     │
│  folder      │     │  Scheduler   │     │  organizer   │
│              │     │  (triggers)  │     │  (classifies │
└──────────────┘     └──────────────┘     │   & moves)   │
                                          └──────────────┘
```

This approach is:
- **Lightweight**: No constant polling or background process
- **Native**: Uses OS built-in infrastructure
- **Reliable**: Task schedulers handle crashes and restarts automatically

### File Name Collision Handling

When moving files, IO_Maid handles name conflicts intelligently:

| Scenario | Action | Example |
|---|---|---|
| **File doesn't exist at destination** | Move normally | `report.pdf` → `_Academic_Papers/report.pdf` |
| **Same name + same size exists** | Delete source (dedup) | `report.pdf` (1.2MB) already exists → source deleted |
| **Same name + different size exists** | Append number | `report.pdf` exists → moved as `report (1).pdf` |
| **Multiple collisions** | Increment counter | `report (1).pdf` exists → moved as `report (2).pdf` |

This ensures:
- **No data loss**: Different files are never overwritten
- **Automatic dedup**: Identical files are cleaned up
- **Unique names**: Every file gets a unique destination

## Category Rules

Files are sorted into these folders:

| Folder | Files |
|---|---|
| `_Applications` | `.app` bundles (macOS) |
| `_Executables` | `.exe`, `.msi` files (Windows) |
| `_WhatsApp` | WhatsApp images, videos, audio, documents |
| `_Screenshots` | Screen shots, untitled diagrams, wallhaven |
| `_Diagrams` | `.drawio` files, drawio backups, page exports |
| `_Installers` | `.dmg` (macOS), `.exe`, `.msi` (Windows) |
| `_Archives` | `.zip`, `.tar`, `.gz`, `.rar`, `.7z` |
| `_Academic_Papers` | `.pdf` files |
| `_Documents` | `.docx` files |
| `_Images` | `.jpg`, `.png`, `.gif`, `.svg`, etc. |
| `_Data` | `.json`, `.csv`, `.py`, `.js`, `.yaml`, etc. |
| `_Text` | `.txt` files |

**Priority order matters**: Files matching multiple categories are assigned to the first matching one. For example, a `WhatsApp Image 2024.jpg` goes to `_WhatsApp`, not `_Images`.

## Custom Configuration

Create a JSON config file to customize categories:

```json
{
    "download_dir": "~/Downloads",
    "categories": [
        {
            "folder": "_MyCategory",
            "conditions": [
                {"type": "ext_in", "values": [".ext1", ".ext2"]}
            ]
        }
    ]
}
```

### Condition Types

| Type | Description | Example |
|---|---|---|
| `ext_equals` | Exact extension match | `{"type": "ext_equals", "value": ".pdf"}` |
| `ext_in` | Extension in list | `{"type": "ext_in", "values": [".jpg", ".png"]}` |
| `name_contains` | Substring in filename | `{"type": "name_contains", "value": "WhatsApp"}` |
| `name_contains_lower` | Case-insensitive substring | `{"type": "name_contains_lower", "value": "_page-0001"}` |
| `name_startswith` | Filename starts with | `{"type": "name_startswith", "values": ["Screenshot"]}` |
| `dir_name_endswith` | Directory name ends with | `{"type": "dir_name_endswith", "value": ".app"}` |

## Running Tests

```bash
# Run all tests
pytest -v

# Run tests for a specific module
pytest tests/test_classifier.py -v
pytest tests/test_mover.py -v
```

## Project Structure

```
IO_Maid/
├── pyproject.toml              # Package config
├── README.md                   # This file
├── AGENTS.md                   # Agent instructions
├── logo.jpg                    # Project logo
├── config/
│   └── default_config.json     # Default classification rules
├── src/io_maid/
│   ├── __init__.py             # Version
│   ├── __main__.py             # python -m io_maid
│   ├── cli.py                  # CLI interface
│   ├── config.py               # Config loading
│   ├── classifier.py           # File classification
│   ├── mover.py                # File moving
│   └── organizer.py            # Main loop
└── tests/                      # Test suite (64 tests)
```

## Changelog

### v1.0.0 (2026-07-17)

**Initial Release**

**Features:**
- Cross-platform support: macOS, Windows, Linux
- 12 category folders: Applications, Executables, WhatsApp, Screenshots, Diagrams, Installers, Archives, Academic Papers, Documents, Images, Data, Text
- Auto-organize via launchd (macOS), Task Scheduler (Windows), cron (Linux)
- Dry-run mode for previewing changes
- Verbose output for debugging
- Custom JSON configuration support
- Deduplication (same name + same size)
- Name collision handling (appends `(1)`, `(2)`, etc.)
- CLI with `--dir`, `--dry-run`, `--verbose`, `--config`, `--install`, `--uninstall`, `--status`

**Technical:**
- Zero runtime dependencies (Python stdlib only)
- src/ layout with pyproject.toml packaging
- 64 tests covering all modules
- pip install from GitHub support

---

<p align="center">
  Made with care by <strong>Boseth Rathnayake</strong>
</p>

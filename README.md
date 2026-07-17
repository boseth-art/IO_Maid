<p align="center">
  <img src="logo.jpg" alt="IO_Maid Logo" width="200"/>
</p>

<h1 align="center">IO_Maid</h1>

<p align="center">
  Auto-organize your Downloads folder by file type and name patterns
</p>

---

## What is IO_Maid?

IO_Maid watches your `~/Downloads` folder and automatically sorts files into organized subfolders based on their type. New downloads are organized within seconds — no manual intervention needed.

## Installation

```bash
cd ~/personal\ project/IO_Maid
pip install -e ".[dev]"
```

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

### Auto-organize (recommended)

Enable automatic organization whenever new files are downloaded:

```bash
# Install the auto-organize agent
io-maid --install

# Check if it's active
io-maid --status

# Disable auto-organize
io-maid --uninstall
```

## Category Rules

Files are sorted into these folders:

| Folder | Files |
|---|---|
| `_Applications` | `.app` bundles |
| `_WhatsApp` | WhatsApp images, videos, audio, documents |
| `_Screenshots` | Screen shots, untitled diagrams, wallhaven |
| `_Diagrams` | `.drawio` files, drawio backups, page exports |
| `_Installers` | `.dmg` files |
| `_Archives` | `.zip`, `.tar`, `.gz`, `.rar`, `.7z` |
| `_Academic_Papers` | `.pdf` files |
| `_Documents` | `.docx` files |
| `_Images` | `.jpg`, `.png`, `.gif`, `.svg`, etc. |
| `_Data` | `.json`, `.csv`, `.py`, `.js`, `.yaml`, etc. |
| `_Text` | `.txt` files |

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
pytest -v
```

## Project Structure

```
IO_Maid/
├── pyproject.toml              # Package config
├── README.md                   # This file
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
└── tests/                      # Test suite
```

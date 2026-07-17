"""Rule-based file classification for IO_Maid."""

from pathlib import Path


def classify(item: Path, config: dict) -> str | None:
    """Return the target folder name for the item, or None to leave in root.

    Classification follows a priority order defined by the categories array
    in the config. The first matching category wins.
    """
    fname = item.name
    ext = item.suffix.lower()

    # Skip system / named files
    if fname in config.get("skip_names", []) or fname.startswith("._"):
        return None

    # Hidden files (except common allowed extensions)
    if fname.startswith(".") and ext not in config.get("hidden_file_extensions", []):
        return None

    # Evaluate categories in priority order
    for category in config.get("categories", []):
        if _matches_category(item, category):
            return category["folder"]

    return None


def _matches_category(item: Path, category: dict) -> bool:
    """Check if an item matches any condition in the category (OR logic)."""
    for condition in category.get("conditions", []):
        if _evaluate_condition(item, condition):
            return True
    return False


def _evaluate_condition(item: Path, condition: dict) -> bool:
    """Evaluate a single condition against an item."""
    ctype = condition["type"]

    if ctype == "ext_equals":
        return item.suffix.lower() == condition["value"]

    if ctype == "ext_in":
        return item.suffix.lower() in condition["values"]

    if ctype == "name_contains":
        # Support both "value" (single string) and "values" (list)
        values = condition.get("values", [])
        if not values and "value" in condition:
            values = [condition["value"]]
        return any(v in item.name for v in values)

    if ctype == "name_contains_lower":
        return condition["value"] in item.name.lower()

    if ctype == "name_startswith":
        return any(item.name.startswith(v) for v in condition["values"])

    if ctype == "dir_name_endswith":
        return item.is_dir() and item.name.endswith(condition["value"])

    return False

"""
Downloads Folder Organizer
Automatically sorts files in your Downloads folder into categorized subfolders.
"""

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────────────────────

DOWNLOADS_FOLDER = Path.home() / "Downloads"

# Map: subfolder name → list of file extensions (lowercase, with dot)
FILE_CATEGORIES = {
    "Images":       [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
                     ".webp", ".ico", ".tiff", ".heic", ".raw"],
    "Videos":       [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv",
                     ".webm", ".m4v", ".mpeg", ".3gp"],
    "Audio":        [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a",
                     ".wma", ".opus", ".aiff"],
    "Documents":    [".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt",
                     ".md", ".pages", ".tex", ".epub", ".mobi"],
    "Spreadsheets": [".xls", ".xlsx", ".ods", ".csv", ".tsv", ".numbers"],
    "Presentations":[".ppt", ".pptx", ".odp", ".key"],
    "Archives":     [".zip", ".tar", ".gz", ".bz2", ".xz", ".7z",
                     ".rar", ".iso", ".dmg", ".tgz"],
    "Code":         [".py", ".js", ".ts", ".html", ".css", ".java",
                     ".c", ".cpp", ".h", ".cs", ".go", ".rs", ".php",
                     ".rb", ".sh", ".bat", ".ps1", ".sql", ".json",
                     ".xml", ".yaml", ".yml", ".toml", ".env"],
    "Executables":  [".exe", ".msi", ".apk", ".deb", ".rpm", ".app",
                     ".pkg", ".run"],
    "Fonts":        [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "Torrents":     [".torrent"],
}

# ── Logging setup ───────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Helpers ─────────────────────────────────────────────────────────────────────

def build_ext_map(categories: dict) -> dict:
    """Return a flat dict: extension → category name."""
    ext_map = {}
    for category, extensions in categories.items():
        for ext in extensions:
            ext_map[ext.lower()] = category
    return ext_map


def safe_destination(dest_folder: Path, filename: str) -> Path:
    """
    Return a destination path that won't overwrite an existing file.
    If 'report.pdf' already exists, returns 'report_2.pdf', 'report_3.pdf', …
    """
    dest = dest_folder / filename
    if not dest.exists():
        return dest

    stem, suffix = Path(filename).stem, Path(filename).suffix
    counter = 2
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        dest = dest_folder / new_name
        if not dest.exists():
            return dest
        counter += 1


def organize(folder: Path, dry_run: bool = False) -> dict:
    """
    Move files in *folder* into category subfolders.

    Args:
        folder:  Path to the Downloads directory.
        dry_run: If True, only log what would happen — don't move anything.

    Returns:
        A summary dict: {category: count_of_files_moved}
    """
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    ext_map   = build_ext_map(FILE_CATEGORIES)
    summary   = {}
    skipped   = []

    log.info("Scanning: %s  (dry_run=%s)", folder, dry_run)

    for item in sorted(folder.iterdir()):
        # Skip subfolders and hidden files
        if item.is_dir():
            continue
        if item.name.startswith("."):
            log.debug("Skipping hidden file: %s", item.name)
            continue

        ext      = item.suffix.lower()
        category = ext_map.get(ext, "Misc")  # unknown extensions → Misc

        dest_folder = folder / category
        dest_path   = safe_destination(dest_folder, item.name)

        if dry_run:
            log.info("[DRY RUN] Would move  %-40s → %s/", item.name, category)
        else:
            dest_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_path))
            log.info("Moved  %-40s → %s/", item.name, category)

        summary[category] = summary.get(category, 0) + 1

    return summary, skipped


def print_summary(summary: dict, dry_run: bool) -> None:
    prefix = "[DRY RUN] " if dry_run else ""
    total  = sum(summary.values())
    print("\n" + "─" * 45)
    print(f"  {prefix}Organization complete — {total} file(s) processed")
    print("─" * 45)
    for category, count in sorted(summary.items(), key=lambda x: -x[1]):
        print(f"  {category:<20} {count:>4} file(s)")
    print("─" * 45 + "\n")


# ── Entry point ──────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Organize your Downloads folder into subfolders by file type."
    )
    parser.add_argument(
        "--folder", "-f",
        type=Path,
        default=DOWNLOADS_FOLDER,
        help=f"Path to the folder to organize (default: {DOWNLOADS_FOLDER})",
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Preview what would be moved without actually moving anything.",
    )
    args = parser.parse_args()

    try:
        summary, _ = organize(args.folder, dry_run=args.dry_run)
        print_summary(summary, dry_run=args.dry_run)
    except FileNotFoundError as e:
        log.error("%s", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
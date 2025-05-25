import shutil
from datetime import datetime, timedelta
from pathlib import Path
from speech2action.config.settings import get_settings
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "speech2action"))

GROUPS = ["chest", "back", "legs", "arms"]


def update_date_in_content(content, new_date):
    """
    Replace or insert a 'date::' line with the new_date (YYYY-MM-DD).
    """
    import re

    lines = content.splitlines()
    date_line = f"date:: {new_date}"
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith("date::"):
            lines[i] = date_line
            found = True
            break
    if not found:
        lines.insert(0, date_line)
    return "\n".join(lines)


def create_gym_dir():
    """
    Create a new gym directory for today in the Weightlifting vault, cycling exercise groups.
    Copy .md files from the previous same-group directory (if exists), updating the date:: line.
    """
    settings = get_settings()
    obsidian_vault_path = settings.OBSIDIAN_EXERCISE_VAULT_PATH
    if not obsidian_vault_path:
        print(
            "[ERROR] OBSIDIAN_EXERCISE_VAULT_PATH is not set. Please set it in your .env file."
        )
        return
    vault = Path(obsidian_vault_path)
    today = datetime.today().date()
    year = today.strftime("%Y")
    year_month = today.strftime("%Y-%m")
    today_str = today.strftime("%Y-%m-%d")
    base_dir = vault / "Weightlifting"

    # Find all gym directories recursively
    gym_dirs = sorted(base_dir.glob("**/*gym *"))
    if not gym_dirs:
        next_group = GROUPS[0]
    else:
        latest_dir = gym_dirs[-1]
        last_group = latest_dir.name.split()[-1]
        try:
            idx = GROUPS.index(last_group)
            next_group = GROUPS[(idx + 1) % len(GROUPS)]
        except ValueError:
            next_group = GROUPS[0]

    # New directory path
    new_dir = base_dir / year / year_month / f"{today_str} gym {next_group}"
    new_dir.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Created directory: {new_dir}")

    # Find previous same-group directory (excluding today)
    prev_group_dirs = [
        d
        for d in gym_dirs
        if d.name.endswith(f"gym {next_group}") and today_str not in d.name
    ]
    prev_group_dir = prev_group_dirs[-1] if prev_group_dirs else None
    if prev_group_dir:
        md_files = list(prev_group_dir.glob("*.md"))
        if md_files:
            for f in md_files:
                content = f.read_text(encoding="utf-8")
                updated_content = update_date_in_content(content, today_str)
                (new_dir / f.name).write_text(updated_content, encoding="utf-8")
            print(
                f"[INFO] Copied .md files from {prev_group_dir} to {new_dir} (date updated)"
            )
        else:
            print(f"[INFO] No .md files to copy from {prev_group_dir}")
    else:
        print(f"[INFO] No previous {next_group} directory found. No files copied.")


def create_note_for_date(
    date_obj,
    note_type: str,
    vault_type: str = "exercise",  # "exercise" or "main"
    base_dir: str = None,  # e.g., "Running", "Mobility", "📆"
    note_prefix: str = None,  # e.g., "Running -", "Mobility -"
    label: str = None,
):
    """
    Generic function to create notes for any type in Obsidian vault.
    Args:
        date_obj: datetime object for the note date
        note_type: Type of note (e.g., "running", "mobility", "daily")
        vault_type: Which vault to use ("exercise" or "main")
        base_dir: Base directory name in the vault
        note_prefix: Prefix for the note filename
        label: Label for logging purposes
    """
    settings = get_settings()
    vault_path = (
        settings.OBSIDIAN_EXERCISE_VAULT_PATH
        if vault_type == "exercise"
        else settings.OBSIDIAN_MAIN_VAULT_PATH
    )
    if not vault_path:
        print(
            f"[ERROR] OBSIDIAN_{vault_type.upper()}_VAULT_PATH is not set. Please set it in your .env file."
        )
        return
    vault = Path(vault_path)
    year = date_obj.strftime("%Y")
    year_month = date_obj.strftime("%Y-%m")
    date_str = date_obj.strftime("%Y-%m-%d")

    # Handle daily notes differently
    if note_type == "daily":
        note_dir = vault / base_dir / year_month
        note_dir.mkdir(parents=True, exist_ok=True)
        note_path = note_dir / f"{date_str}.md"
        # Check for template
        template_path = vault / "Templates" / "Daily Note Template.md"
        if template_path.exists():
            content = template_path.read_text(encoding="utf-8")
            note_path.write_text(content, encoding="utf-8")
            print(
                f"[INFO] Created {label}'s note {note_path} from template {template_path}"
            )
        else:
            note_path.touch(exist_ok=True)
            print(
                f"[INFO] Created blank {label}'s note {note_path} (no template found)"
            )
        return

    # For exercise notes
    note_dir = vault / base_dir / year / year_month
    note_dir.mkdir(parents=True, exist_ok=True)
    note_path = note_dir / f"{note_prefix} {date_str}.md"
    # Find all previous notes in all subfolders (exclude today)
    all_notes = sorted(vault.glob(f"{base_dir}/*/*/{note_prefix} *.md"))
    prev_notes = [n for n in all_notes if n.stem != f"{note_prefix} {date_str}"]
    if prev_notes:

        def note_date(note):
            try:
                return datetime.strptime(
                    note.stem.replace(f"{note_prefix} ", ""), "%Y-%m-%d"
                )
            except Exception:
                return datetime.min

        latest_note = max(prev_notes, key=note_date)
        content = latest_note.read_text(encoding="utf-8")
        updated_content = update_date_in_content(content, date_str)
        note_path.write_text(updated_content, encoding="utf-8")
        print(
            f"[INFO] Created {note_type} note: {note_path} (copied from {latest_note}, date updated)"
        )
    else:
        note_path.write_text(f"date:: {date_str}\n", encoding="utf-8")
        print(f"[INFO] Created blank {note_type} note: {note_path}")


def create_daily_note():
    create_note_for_date(
        date_obj=datetime.today().date(),
        note_type="daily",
        vault_type="main",
        base_dir="\U0001f4c6",  # 📆
        label="today",
    )


def create_tomorrow_note():
    create_note_for_date(
        date_obj=datetime.today().date() + timedelta(days=1),
        note_type="daily",
        vault_type="main",
        base_dir="\U0001f4c6",  # 📆
        label="tomorrow",
    )


def create_today_running_note():
    create_note_for_date(
        date_obj=datetime.today().date(),
        note_type="running",
        vault_type="exercise",
        base_dir="Running",
        note_prefix="Running -",
        label="running",
    )


def create_today_stairclimbing_note():
    create_note_for_date(
        date_obj=datetime.today().date(),
        note_type="stairclimbing",
        vault_type="exercise",
        base_dir="Stairclimbing",
        note_prefix="Stair climbing",
        label="stairclimbing",
    )


def create_today_mobility_note():
    create_note_for_date(
        date_obj=datetime.today().date(),
        note_type="mobility",
        vault_type="exercise",
        base_dir="Mobility",
        note_prefix="Mobility -",
        label="mobility",
    )


def create_today_cycling_note():
    create_note_for_date(
        date_obj=datetime.today().date(),
        note_type="cycling",
        vault_type="exercise",
        base_dir="Cycling",
        note_prefix="Cycling -",
        label="cycling",
    )

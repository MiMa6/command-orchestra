import shutil
from datetime import datetime, timedelta
from pathlib import Path
from speech2action.config.settings import get_settings
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "speech2action"))

GROUPS = ["chest", "back", "legs", "arms"]


def create_gym_dir():
    """
    Create a new gym directory for today in the Weightlifting vault, cycling exercise groups.
    Copy .md files from the previous same-group directory (if exists).
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
                shutil.copy2(f, new_dir)
            print(f"[INFO] Copied .md files from {prev_group_dir} to {new_dir}")
        else:
            print(f"[INFO] No .md files to copy from {prev_group_dir}")
    else:
        print(f"[INFO] No previous {next_group} directory found. No files copied.")


def create_daily_note_for_date(date_obj, label="today"):
    """
    Create a daily note for the given date in the main Obsidian vault under 📆/<year-month>/<year-month-day>.md
    Apply the daily template from Templates/Daily Note Template.md if it exists.
    """
    settings = get_settings()
    obsidian_vault_path = getattr(settings, "OBSIDIAN_MAIN_VAULT_PATH", None)
    if not obsidian_vault_path:
        print(
            f"[ERROR] OBSIDIAN_MAIN_VAULT_PATH is not set. Please set it in your .env file."
        )
        return
    vault = Path(obsidian_vault_path)
    year_month = date_obj.strftime("%Y-%m")
    date_str = date_obj.strftime("%Y-%m-%d")
    calendar_dir = vault / "📆" / year_month
    calendar_dir.mkdir(parents=True, exist_ok=True)
    note_path = calendar_dir / f"{date_str}.md"

    # Check for template in Templates/Daily Note Template.md
    template_path = vault / "Templates" / "Daily Note Template.md"
    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
        note_path.write_text(content, encoding="utf-8")
        print(
            f"[INFO] Created {label}'s note {note_path} from template {template_path}"
        )
    else:
        note_path.touch(exist_ok=True)
        print(f"[INFO] Created blank {label}'s note {note_path} (no template found)")


def create_daily_note():
    create_daily_note_for_date(datetime.today().date(), label="today")


def create_tomorrow_note():
    create_daily_note_for_date(
        datetime.today().date() + timedelta(days=1), label="tomorrow"
    )

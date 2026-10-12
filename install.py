#!/usr/bin/env python3
"""Install or remove the Claude Code status line.

Install (from a clone):
    python3 install.py --budget 200

Install (one line, no clone needed):
    curl -fsSL https://raw.githubusercontent.com/OWNER/claude-statusline/main/install.py | python3 - --budget 200

Remove:
    python3 install.py --uninstall
"""
import argparse
import json
import os
import shutil
import sys
import urllib.request
from datetime import datetime

REPO_RAW = "https://raw.githubusercontent.com/OWNER/claude-statusline/main"
CLAUDE_DIR = os.path.expanduser("~/.claude")
SETTINGS = os.path.join(CLAUDE_DIR, "settings.json")
SCRIPT = os.path.join(CLAUDE_DIR, "statusline.py")
REFRESH_SECONDS = 10


def load_settings():
    if not os.path.exists(SETTINGS):
        return {}
    with open(SETTINGS, encoding="utf-8") as f:
        text = f.read()
    if not text.strip():
        return {}
    try:
        return json.loads(text)
    except ValueError as e:
        sys.exit(f"Cannot parse {SETTINGS}: {e}\nFix or remove it, then run again.")


def save_settings(settings):
    os.makedirs(CLAUDE_DIR, exist_ok=True)
    if os.path.exists(SETTINGS):
        backup = f"{SETTINGS}.bak-{datetime.now():%Y%m%d-%H%M%S}"
        shutil.copy2(SETTINGS, backup)
        print(f"Backed up settings to {backup}")
    with open(SETTINGS, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")


def fetch_script():
    """Use statusline.py next to this file, or download it when run via curl."""
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "statusline.py")
    if os.path.exists(local):
        shutil.copy2(local, SCRIPT)
    else:
        with urllib.request.urlopen(f"{REPO_RAW}/statusline.py", timeout=30) as r:
            with open(SCRIPT, "wb") as f:
                f.write(r.read())
    os.chmod(SCRIPT, 0o755)


def install(budget):
    settings = load_settings()
    old = settings.get("statusLine")
    if old and SCRIPT not in json.dumps(old):
        print(f"Replacing existing statusLine: {json.dumps(old)}")

    fetch_script()
    settings["statusLine"] = {
        "type": "command",
        "command": f"{sys.executable} -I {SCRIPT}",
        "refreshInterval": REFRESH_SECONDS,
    }
    if budget is not None:
        env = settings.setdefault("env", {})
        env["CLAUDE_MONTHLY_BUDGET_USD"] = f"{budget:g}"
    save_settings(settings)

    print(f"Installed {SCRIPT}")
    if budget is None:
        print("No budget set: the monthly bar will show spend only.\n"
              "Set it later with: python3 install.py --budget 200")
    print("Restart Claude Code (or open a new session) and accept the workspace trust prompt.")


def uninstall():
    settings = load_settings()
    if SCRIPT in json.dumps(settings.get("statusLine", "")):
        del settings["statusLine"]
        env = settings.get("env", {})
        env.pop("CLAUDE_MONTHLY_BUDGET_USD", None)
        if not env:
            settings.pop("env", None)
        save_settings(settings)
        print("Removed statusLine and budget from settings.json")
    else:
        print("statusLine in settings.json is not ours; left unchanged")
    if os.path.exists(SCRIPT):
        os.remove(SCRIPT)
        print(f"Removed {SCRIPT}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--budget", type=float, help="monthly budget in USD for the 1m bar")
    parser.add_argument("--uninstall", action="store_true", help="remove the status line")
    args = parser.parse_args()
    if args.uninstall:
        uninstall()
    else:
        if args.budget is not None and args.budget <= 0:
            sys.exit("--budget must be greater than 0")
        install(args.budget)


if __name__ == "__main__":
    main()

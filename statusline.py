#!/usr/bin/env python3
"""Claude Code status line.

Line 1: model name, 5h and 7d subscription quota bars, monthly spend bar.
Line 2: current working directory, truncated with an ellipsis so it never wraps.

5h / 7d come from the official `rate_limits` field (claude.ai subscriptions only).
Monthly is API-equivalent spend this month vs. CLAUDE_MONTHLY_BUDGET_USD, because
subscriptions have no monthly quota. Session costs are recorded in a small ledger.
"""
import json
import os
import sys
import unicodedata
from datetime import datetime, timezone

LEDGER = os.path.expanduser("~/.claude/statusline-ledger.json")
BAR_WIDTH = 10
RESET = "\033[0m"
DIM = "\033[2m"


def color(pct):
    if pct >= 90:
        return "\033[31m"  # red
    if pct >= 70:
        return "\033[33m"  # yellow
    return "\033[32m"      # green


def bar(pct):
    pct = max(0.0, min(100.0, pct))
    filled = round(pct / 100 * BAR_WIDTH)
    return f"{color(pct)}{'█' * filled}{DIM}{'░' * (BAR_WIDTH - filled)}{RESET}"


def fmt_left(resets_at):
    """Time until a quota window resets, e.g. ' ↻4h22m'. Accepts epoch seconds or ISO 8601."""
    if not resets_at:
        return ""
    try:
        if isinstance(resets_at, (int, float)):
            end = datetime.fromtimestamp(resets_at, timezone.utc)
        else:
            end = datetime.fromisoformat(resets_at.replace("Z", "+00:00"))
    except (TypeError, ValueError, OverflowError):
        return ""
    secs = int((end - datetime.now(timezone.utc)).total_seconds())
    if secs <= 0:
        return " ↻now"
    h, rem = divmod(secs, 3600)
    d, h = divmod(h, 24)
    if d:
        return f" ↻{d}d{h}h"
    return f" ↻{h}h{rem // 60:02d}m"


def term_columns():
    for fd in (1, 2, 0):
        try:
            return os.get_terminal_size(fd).columns
        except OSError:
            pass
    try:
        return int(os.environ["COLUMNS"])
    except (KeyError, ValueError):
        return 80


def char_width(ch):
    return 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1


def fit(text, max_width):
    """Truncate to max_width display columns, appending … when cut."""
    if sum(char_width(c) for c in text) <= max_width:
        return text
    out, used = [], 0
    for c in text:
        w = char_width(c)
        if used + w > max_width - 1:
            break
        out.append(c)
        used += w
    return "".join(out) + "…"


def segment(label, pct, extra=""):
    return f"{label} {bar(pct)} {color(pct)}{pct:3.0f}%{RESET}{DIM}{extra}{RESET}"


def update_ledger(session_id, cost, month):
    """Keep the max cost seen per session in the current month; drop older months."""
    try:
        with open(LEDGER) as f:
            ledger = json.load(f)
    except (OSError, ValueError):
        ledger = {}
    ledger = {m: v for m, v in ledger.items() if m == month}
    sessions = ledger.setdefault(month, {})
    if session_id:
        sessions[session_id] = max(cost, sessions.get(session_id, 0.0))
    try:
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        tmp = LEDGER + ".tmp"
        with open(tmp, "w") as f:
            json.dump(ledger, f)
        os.replace(tmp, LEDGER)
    except OSError:
        pass  # Display still works if the ledger cannot be written.
    return sum(sessions.values())


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}

    parts = []
    model = (data.get("model") or {}).get("display_name")
    if model:
        parts.append(f"{DIM}{model}{RESET}")
    limits = data.get("rate_limits") or {}
    five = limits.get("five_hour") or {}
    week = limits.get("seven_day") or {}
    if five.get("used_percentage") is not None:
        parts.append(segment("5h", five["used_percentage"], fmt_left(five.get("resets_at"))))
    if week.get("used_percentage") is not None:
        parts.append(segment("7d", week["used_percentage"], fmt_left(week.get("resets_at"))))

    month = datetime.now().strftime("%Y-%m")
    cost = float((data.get("cost") or {}).get("total_cost_usd") or 0.0)
    spent = update_ledger(data.get("session_id"), cost, month)
    try:
        budget = float(os.environ.get("CLAUDE_MONTHLY_BUDGET_USD", ""))
    except ValueError:
        budget = 0.0
    if budget > 0:
        parts.append(segment("1m", spent / budget * 100, f" ${spent:.2f}/${budget:.0f}"))
    else:
        parts.append(f"{DIM}1m ${spent:.2f} (set CLAUDE_MONTHLY_BUDGET_USD){RESET}")

    print("  ".join(parts))

    cwd = data.get("cwd") or (data.get("workspace") or {}).get("current_dir") or os.getcwd()
    home = os.path.expanduser("~")
    if cwd == home or cwd.startswith(home + os.sep):
        cwd = "~" + cwd[len(home):]
    # One column short of the terminal width so the line never wraps.
    print(f"{DIM}{fit(cwd, term_columns() - 1)}{RESET}")


if __name__ == "__main__":
    main()

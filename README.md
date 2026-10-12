# claude-statusline

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh-CN.md)

A status line for Claude Code. The first line shows the model and quota bars; the second line shows the current directory.

```
Haiku 5.5  5h ██░░░░░░░░  20% ↻4h22m  7d █████████░  91% ↻3d15h  1m ░░░░░░░░░░   6% $1.20/$20
/home/user/projects/my-app
```

- **Model**: the model currently in use.
- **5h / 7d**: subscription quota usage as a percentage, with time until the window resets (claude.ai subscribers only).
- **1m**: this month's API-equivalent spend as a share of your budget (see below).
- **Directory**: the working directory. The home directory is shown as `~`. If it is wider than the terminal, it is cut with `…` and never wraps.
- Colors: green below 70%, yellow from 70% to 90%, red at 90% and above.

## Install

Requires Python 3.8+ and Claude Code.

One-line install (no clone needed):

```sh
curl -fsSL https://raw.githubusercontent.com/IceThunder/claude-statusline/main/install.py | python3 - --budget 200
```

Or clone first:

```sh
git clone https://github.com/IceThunder/claude-statusline.git
cd claude-statusline
python3 install.py --budget 200
```

`--budget` is your monthly budget in USD, used by the 1m bar. Without it, the bar shows spend only.

After installing, restart Claude Code or open a new session. The first time you open a directory, Claude Code asks whether to trust it. **The status line only runs after you accept that prompt.**

## How it works

- The installer copies `statusline.py` to `~/.claude/` and adds a `statusLine` entry to `~/.claude/settings.json` with `refreshInterval` set to 10 seconds.
- Before changing `settings.json`, the installer saves a backup named `settings.json.bak-<timestamp>`.
- The 5h and 7d figures come from the `rate_limits` field that Claude Code passes to the status line.
- Subscriptions have no monthly quota. The 1m bar adds up each session's `total_cost_usd` for the month. It only counts sessions that ran this status line, so treat it as an estimate. The ledger is stored at `~/.claude/statusline-ledger.json`.

## Change the budget

Run the install command again with a new value:

```sh
python3 install.py --budget 300
```

## Uninstall

```sh
python3 install.py --uninstall
```

This removes the `statusLine` entry, the budget variable, and `~/.claude/statusline.py`. The ledger and backup files are kept.

## Test

```sh
python3 -m unittest discover -s tests -v
```

## License

MIT

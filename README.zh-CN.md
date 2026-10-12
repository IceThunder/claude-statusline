# claude-statusline

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | **中文**

Claude Code 底部状态栏，一行显示模型和额度进度条，下一行显示当前目录。

```
Haiku 5.5  5h ██░░░░░░░░  20% ↻4h22m  7d █████████░  91% ↻3d15h  1m ░░░░░░░░░░   6% $1.20/$20
/home/user/projects/my-app
```

- **模型名**：当前使用的模型。
- **5h / 7d**：订阅额度的使用百分比和距离重置的时间（仅 claude.ai 订阅用户可见）。
- **1m**：本月的 API 等价花费占你设定预算的比例（见下文说明）。
- **目录**：当前工作目录，家目录显示为 `~`，超出终端宽度时以 `…` 截断，不换行。
- 颜色：低于 70% 绿色，70–90% 黄色，90% 以上红色。

## 安装

需要 Python 3.8+ 和 Claude Code。

一行安装（不需要先 clone）：

```sh
curl -fsSL https://raw.githubusercontent.com/IceThunder/claude-statusline/main/install.py | python3 - --budget 200
```

或者 clone 后安装：

```sh
git clone https://github.com/IceThunder/claude-statusline.git
cd claude-statusline
python3 install.py --budget 200
```

`--budget` 是你每月希望的预算（美元），用于 1m 进度条。不传则只显示本月花费。

安装后重启 Claude Code 或新开一个会话。第一次进入目录时，Claude Code 会询问是否信任该工作区，**信任后状态栏才会运行**。

## 工作原理

- 安装器会把 `statusline.py` 复制到 `~/.claude/`，并在 `~/.claude/settings.json` 中添加 `statusLine` 配置，`refreshInterval` 为 10 秒。
- 修改 `settings.json` 前会先备份为 `settings.json.bak-时间戳`。
- 5h / 7d 数据来自 Claude Code 传给状态栏的 `rate_limits` 字段。
- 订阅没有月度额度。1m 进度条按本月每个会话的 `total_cost_usd` 累计，只统计使用过本状态栏的会话，属于估算值。账本保存在 `~/.claude/statusline-ledger.json`。

## 修改预算

重新运行安装命令即可：

```sh
python3 install.py --budget 300
```

## 卸载

```sh
python3 install.py --uninstall
```

会删除 `statusLine` 配置、预算变量和 `~/.claude/statusline.py`。账本文件和备份文件不会自动删除。

## 测试

```sh
python3 -m unittest discover -s tests -v
```

## 许可证

MIT

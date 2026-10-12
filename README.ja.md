# claude-statusline

[English](README.md) | [한국어](README.ko.md) | **日本語** | [中文](README.zh-CN.md)

Claude Code の下部ステータスラインです。1 行目にモデルと利用枠のバーを、2 行目に現在のディレクトリを表示します。

```
Haiku 5.5  5h ██░░░░░░░░  20% ↻4h22m  7d █████████░  91% ↻3d15h  1m ░░░░░░░░░░   6% $1.20/$20
/home/user/projects/my-app
```

- **モデル**: 現在使用中のモデルです。
- **5h / 7d**: サブスクリプションの利用枠の使用率（%）と、リセットまでの残り時間です（claude.ai のサブスクリプション利用者のみ表示）。
- **1m**: 今月の API 換算コストが設定した予算に占める割合です（下記参照）。
- **ディレクトリ**: 作業ディレクトリです。ホームディレクトリは `~` と表示されます。ターミナルの幅を超える場合は `…` で省略され、折り返しはしません。
- 色: 70% 未満は緑、70〜90% は黄、90% 以上は赤です。

## インストール

Python 3.8 以上と Claude Code が必要です。

ワンライン インストール（リポジトリのクローンは不要）:

```sh
curl -fsSL https://raw.githubusercontent.com/IceThunder/claude-statusline/main/install.py | python3 - --budget 200
```

または、先にクローンしてからインストール:

```sh
git clone https://github.com/IceThunder/claude-statusline.git
cd claude-statusline
python3 install.py --budget 200
```

`--budget` は月の予算（USD）で、1m バーに使われます。指定しない場合は今月の支出のみ表示します。

インストール後、Claude Code を再起動するか新しいセッションを開いてください。ディレクトリを初めて開くと、Claude Code が信頼するかどうかを尋ねます。**この確認を承認した後にのみステータスラインが動作します。**

## 仕組み

- インストーラーは `statusline.py` を `~/.claude/` にコピーし、`~/.claude/settings.json` に `statusLine` の設定を追加します（`refreshInterval` は 10 秒）。
- `settings.json` を変更する前に、`settings.json.bak-<タイムスタンプ>` という名前でバックアップを作成します。
- 5h と 7d の数値は、Claude Code がステータスラインに渡す `rate_limits` の値から取得しています。
- サブスクリプションには月間の上限がありません。1m バーは各セッションの `total_cost_usd` を今月分として合計します。このステータスラインを実行したセッションのみが集計対象なので、目安としてご覧ください。記録は `~/.claude/statusline-ledger.json` に保存されます。

## 予算の変更

新しい値を指定してインストールコマンドを再実行します:

```sh
python3 install.py --budget 300
```

## アンインストール

```sh
python3 install.py --uninstall
```

`statusLine` の設定、予算の環境変数、`~/.claude/statusline.py` が削除されます。記録ファイルとバックアップファイルは残ります。

## テスト

```sh
python3 -m unittest discover -s tests -v
```

## ライセンス

MIT

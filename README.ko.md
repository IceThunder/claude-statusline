# claude-statusline

[English](README.md) | **한국어** | [日本語](README.ja.md) | [中文](README.zh-CN.md)

Claude Code 하단 상태 표시줄입니다. 첫 번째 줄에는 모델과 사용량 진행 막대가, 두 번째 줄에는 현재 디렉터리가 표시됩니다.

```
Haiku 5.5  5h ██░░░░░░░░  20% ↻4h22m  7d █████████░  91% ↻3d15h  1m ░░░░░░░░░░   6% $1.20/$20
/home/user/projects/my-app
```

- **모델**: 현재 사용 중인 모델입니다.
- **5h / 7d**: 구독 사용량을 백분율로 표시하고, 기간이 재설정되기까지 남은 시간을 함께 보여줍니다 (claude.ai 구독자만 표시됨).
- **1m**: 이번 달 API 환산 비용이 설정한 예산에서 차지하는 비율입니다 (아래 설명 참고).
- **디렉터리**: 작업 디렉터리입니다. 홈 디렉터리는 `~`로 표시됩니다. 터미널 너비를 넘으면 `…`으로 잘리며 줄바꿈되지 않습니다.
- 색상: 70% 미만은 초록, 70–90%는 노랑, 90% 이상은 빨강입니다.

## 설치

Python 3.8 이상과 Claude Code가 필요합니다.

한 줄 설치 (저장소를 복제할 필요 없음):

```sh
curl -fsSL https://raw.githubusercontent.com/IceThunder/claude-statusline/main/install.py | python3 - --budget 200
```

또는 먼저 복제한 뒤 설치:

```sh
git clone https://github.com/IceThunder/claude-statusline.git
cd claude-statusline
python3 install.py --budget 200
```

`--budget`은 월 예산(USD)으로, 1m 막대에 사용됩니다. 지정하지 않으면 이번 달 지출만 표시됩니다.

설치 후 Claude Code를 재시작하거나 새 세션을 여세요. 디렉터리를 처음 열면 Claude Code가 신뢰 여부를 묻습니다. **이 질문을 수락해야 상태 표시줄이 실행됩니다.**

## 동작 방식

- 설치 프로그램은 `statusline.py`를 `~/.claude/`에 복사하고, `~/.claude/settings.json`에 `statusLine` 항목을 추가합니다 (`refreshInterval`은 10초).
- `settings.json`을 수정하기 전에 `settings.json.bak-<타임스탬프>` 형식으로 백업합니다.
- 5h, 7d 수치는 Claude Code가 상태 표시줄에 전달하는 `rate_limits` 값에서 가져옵니다.
- 구독에는 월간 한도가 없습니다. 1m 막대는 세션별 `total_cost_usd`를 이번 달 기준으로 합산합니다. 이 상태 표시줄을 실행한 세션만 집계하므로 추정치로 보세요. 기록은 `~/.claude/statusline-ledger.json`에 저장됩니다.

## 예산 변경

새 값으로 설치 명령을 다시 실행하세요:

```sh
python3 install.py --budget 300
```

## 제거

```sh
python3 install.py --uninstall
```

`statusLine` 항목, 예산 변수, `~/.claude/statusline.py`가 제거됩니다. 기록 파일과 백업 파일은 남겨둡니다.

## 테스트

```sh
python3 -m unittest discover -s tests -v
```

## 라이선스

MIT

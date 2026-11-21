# Tactical Lantern

[中文](#中文) · [English](#english)

## 中文

用于小型国际象棋赛的确定性 Python 引擎，使用标准库并通过赛事接口读取对局。

### 本地运行

使用 Python 3.13。运行 `python demo.py`，引擎会从初始棋局的四个候选着法中选一步。参加对局时，将 `MAKEFUN_ENV_URL` 指向赛事环境，再执行 `python main.py`。

## English

A deterministic, standard-library Python chess engine for the tiny-chess challenge.

### Run locally

Use Python 3.13. Run `python demo.py` for a move selected from four candidates in the initial position. For challenge play, set `MAKEFUN_ENV_URL` to the match environment and run `python main.py`.

[补充技术说明 / Additional technical notes](README.details.md)

[make.fun 赛事 / Original bounty](https://make.fun/bounty/tiny-chess-01)

## 许可证 / License

MIT. See [LICENSE](LICENSE).


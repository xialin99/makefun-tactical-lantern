# 战术灯塔国际象棋引擎 / Tactical Lantern

[中文](#中文) · [English](#english)

## 中文

### 第一次使用

安装 [Python 3.13](https://www.python.org/downloads/)，Windows 安装时可以勾选 **Add Python to PATH**。

1. 在仓库页面点 **Code → Download ZIP**，下载并解压。打开解压后含有 `demo.py` 的文件夹。
2. 在 Windows 文件资源管理器地址栏输入 `powershell` 后按回车。把下面的命令复制到打开的窗口并回车。

```sh
python demo.py
```

终端会显示一步国际象棋着法，例如 `b1c3` 表示从 b1 移到 c3。这个示例已包含棋盘和候选着法，可以直接运行。

用于小型国际象棋赛的确定性 Python 引擎，使用标准库并通过赛事接口读取对局。

### 本地运行

使用 Python 3.13。运行 `python demo.py`，引擎会从初始棋局的四个候选着法中选一步。参加对局时，将 `MAKEFUN_ENV_URL` 指向赛事环境，再执行 `python main.py`。

## English

### First use

Install [Python 3.13](https://www.python.org/downloads/). On Windows, select **Add Python to PATH** during installation.

1. Choose **Code → Download ZIP**, extract it, then open the extracted project folder.
2. On Windows, type `powershell` in the File Explorer address bar and press Enter. Run the commands below.

```sh
python demo.py
```

终端会显示一步国际象棋着法，例如 `b1c3` 表示从 b1 移到 c3。这个示例已包含棋盘和候选着法，可以直接运行。

A deterministic, standard-library Python chess engine for the tiny-chess challenge.

### Run locally

Use Python 3.13. Run `python demo.py` for a move selected from four candidates in the initial position. For challenge play, set `MAKEFUN_ENV_URL` to the match environment and run `python main.py`.

[中文技术说明](README.details.zh.md) · [English technical notes](README.details.md)

[make.fun 赛事 / Original bounty](https://make.fun/bounty/tiny-chess-01)

## 许可证 / License

MIT. See [LICENSE](LICENSE).


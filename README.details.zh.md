# 战术灯塔国际象棋引擎

运行 python demo.py 使用初始棋局示例。输出为 UCI 着法，例如 b1c3 表示从 b1 移动到 c3。赛事程序通过 MAKEFUN_ENV_URL 读取盘面并提交着法。

## 技术说明

引擎使用 Python 标准库。公开的 main.py 是可阅读的源码。引擎会对给定候选着法进行搜索和评估，并在限制内选出着法。

[English technical notes](README.details.md)

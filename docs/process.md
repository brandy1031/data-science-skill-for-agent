# 过程记录

## 目标

创建一个可复用的 Codex skill，用来处理 data analysis / data science 相关任务，并把刚才的创建和验证过程整理成一个可以在 PyCharm 里打开的 Python 项目。

## 关键环境问题

在 Codex 的非交互 shell 里，直接运行：

```bash
python3
```

解析到的是 macOS 自带的 CommandLineTools Python：

```text
/Library/Developer/CommandLineTools/usr/bin/python3
```

这个解释器里没有 `pandas`，所以第一次运行 `profile_table.py` 失败了。

你的 conda base Python 是：

```text
/opt/anaconda3/bin/python
```

这个环境里有：

```text
pandas 2.3.2
PyYAML 6.0.2
```

所以后续测试都应该显式使用这个解释器，或者确保终端已经激活 conda base。

## 已经验证通过的命令

```bash
/opt/anaconda3/bin/python -c "import sys; print(sys.executable); import pandas as pd; print(pd.__version__)"
/opt/anaconda3/bin/python src/check_environment.py
/opt/anaconda3/bin/python src/profile_table.py data/sample.csv --out data/profile.json
```

## 创建的 skill

已安装的 Codex skill 在这里：

```text
/Users/yaya/.codex/skills/data-science
```

这个 PyCharm 项目里也保留了一份快照：

```text
skill_snapshot/
```

## 以后怎么避免这个问题

做数据分析任务时，不要默认相信 `python3` 一定指向 conda base。更稳的方式是直接使用：

```text
/opt/anaconda3/bin/python
```

在 PyCharm 里也把项目解释器设置成这个路径。


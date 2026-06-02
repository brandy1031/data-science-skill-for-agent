# Data Science Skill 项目

该项目里包括创建Codex `data-science` skill 的过程。


## 项目里有什么

- `src/profile_table.py`：从 skill 里提取出来的数据表快速概览脚本
- `data/sample.csv`：测试用的小样例数据
- `data/profile.json`：样例数据跑出来的概览结果
- `docs/process.md`：这次创建、测试、排查 Python 环境的过程记录
- `skill_snapshot/`：已经安装到 Codex 的 `data-science` skill主要内容，包括skill.md文件


## 在 PyCharm 里运行

1. 打开项目文件夹。
2. 把项目解释器设置为 `/opt/anaconda3/bin/python`。
3. 先运行 `src/check_environment.py`，确认当前环境是 conda base。
4. 再运行 `src/profile_table.py`，参数填：

```text
data/sample.csv --out data/profile.json
```


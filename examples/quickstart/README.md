# Quickstart Demo

这是 MathModel Skill 的最小可跑示例，用来验证 Trae、Claude Code、Codex 三端 skill 包是否安装正确。

本示例不是正式数学建模赛题，只用于演示完整链路：

```text
赛题解析 -> 模型路线 -> 数据与图表计划 -> 数据清洗 -> 论文级图表草稿 -> QA -> 微单元 -> Word
```

## 示例文件

```text
examples/quickstart/
└── problem_files/
    ├── sample_problem.txt
    └── sample_data.csv
```

## 使用方式

1. 新建一个空项目目录，例如 `my-mm-demo/`。
2. 按你的 Agent 平台复制对应 skill 包。
3. 把本目录下的 `problem_files/` 复制到 `my-mm-demo/problem_files/`。
4. 在 `my-mm-demo/` 根目录运行对应一键命令。

Trae:

```bash
python .trae/skills/paper-workflow-orchestrator/scripts/run_all.py
```

Claude Code:

```bash
python .claude/skills/paper-workflow-orchestrator/scripts/run_all.py
```

Codex:

```bash
python skills/paper-workflow-orchestrator/scripts/run_all.py
```

## 期望输出

成功后应生成：

```text
paper_output/
├── step1/problem_analysis.json
├── plan/model_route.json
├── plan/data_plan.json
├── plan/visualization_plan.json
├── figure_index.json
├── tasks.json
├── final_paper.md
├── final_paper.docx
├── ref_check.md
├── data_cleaned/
└── figures/
```

其中 `paper_output/figures/fig_q*.png` 是按图表计划生成的论文级草稿图。真实赛题中应把当前模型输出接入这些模板，再二次修改。

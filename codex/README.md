# MathModel Skill for Codex

这是 MathModel Skill 的 Codex 原生包。

本目录按完整 skill 包分发。每个 skill 都是一个文件夹，包含 `SKILL.md` 和可选的 `scripts/`、`references/`、`assets/` 等资源。

```text
codex/
├── AGENTS.md
└── skills/
    ├── problem-doc-model-selector/
    ├── modeling-paper-rubric-and-model-selector/
    ├── authoritative-data-harvester/
    ├── data-cleaning-and-visualization/
    ├── quality-assurance-auditor/
    ├── paper-micro-unit-generator/
    ├── paper-workflow-orchestrator/
    └── context-memory-keeper/
```

## 安装方式

把 `codex/skills/` 中的 skill 文件夹复制到你的 Codex skills 目录，或复制到项目根目录作为项目内 skills：

```text
your-mathmodel-project/
└── skills/
```

如果你希望 Codex 在项目里自动了解工作流，也复制：

```text
codex/AGENTS.md -> your-mathmodel-project/AGENTS.md
```

## 使用方式

在项目根目录准备输入目录：

```text
problem_files/      # 放赛题 PDF/Word 和官方附件数据
crawled_data/       # 可选，放外部补充数据
```

然后让 Codex 使用：

```text
使用 paper-workflow-orchestrator，开始生成数学建模论文。
```

也可以直接运行：

```bash
python skills/paper-workflow-orchestrator/scripts/run_all.py
```

## 输出位置

```text
paper_output/final_paper.docx
paper_output/final_paper.md
paper_output/tasks.json
paper_output/ref_check.md
paper_output/data_cleaned/
paper_output/figures/
```

## 说明

- Codex 包基于 Trae 原版 skill 包适配。
- 适配只改变平台路径和平台称呼，不改变工作流设计。
- 每个 skill 都是完整文件夹，保留脚本和参考材料。

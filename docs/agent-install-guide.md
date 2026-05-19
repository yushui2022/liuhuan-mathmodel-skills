# Agent 安装指南

MathModel Skill 按完整 skill 包分发。请选择你使用的 Agent 平台，只复制对应目录即可。

| Agent | 复制来源 | 复制到项目内 | 原生入口 | 一键命令 |
|---|---|---|---|---|
| Trae | `packages/trae/.trae/skills/` | `.trae/skills/` | `.trae/skills/*/SKILL.md` | `python .trae/skills/paper-workflow-orchestrator/scripts/run_all.py` |
| Claude Code | `packages/claude/.claude/skills/` + `packages/claude/CLAUDE.md` | `.claude/skills/` + `CLAUDE.md` | `.claude/skills/*/SKILL.md` | `python .claude/skills/paper-workflow-orchestrator/scripts/run_all.py` |
| Codex | `packages/codex/skills/` + `packages/codex/AGENTS.md` | `skills/` + `AGENTS.md` | `skills/*/SKILL.md` | `python skills/paper-workflow-orchestrator/scripts/run_all.py` |

## 输入目录

所有平台都使用相同输入目录：

```text
problem_files/      # 赛题 PDF/Word 和官方附件数据
crawled_data/       # 可选，外部补充数据
```

## 输出目录

所有平台都使用相同输出目录：

```text
paper_output/
├── final_paper.docx
├── final_paper.md
├── tasks.json
├── ref_check.md
├── data_cleaned/
└── figures/
```

## Skill 包结构

每个 skill 都是完整文件夹，不是单个 Markdown：

```text
skill-name/
├── SKILL.md
├── scripts/
├── references/
├── assets/
└── 其他资源
```

其中 `scripts/`、`references/`、`assets/` 不是每个 skill 都必有，但如果原版存在，平台包中会完整保留。

## 更新方式

后续更新时，重新复制对应平台目录即可：

```text
Trae        -> packages/trae/.trae/skills/
Claude Code -> packages/claude/.claude/skills/
Codex       -> packages/codex/skills/
```

如果你修改过本地 skill，请先备份再覆盖。

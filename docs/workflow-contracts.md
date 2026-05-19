# Workflow Contracts

MathModel Skill 使用少量 JSON 文件作为不同 skill 之间的结构化交接单。这些文件不是 Trae、Claude Code 或 Codex 的平台标准，而是本项目自己的 workflow contract。

JSON 只保存后续环节必须稳定读取的结构化信息；长篇解释、写作策略和提示词仍放 Markdown 或 `references/`。

## Contract List

| Contract | Producer | Consumers | Purpose |
|---|---|---|---|
| `paper_output/step1/problem_analysis.json` | `problem-doc-model-selector` | 模型路线、QA、微单元生成 | 保存结构化题意分析、子问题、任务类型、数据附件画像 |
| `paper_output/plan/model_route.json` | `modeling-paper-rubric-and-model-selector` | QA、微单元生成 | 保存每一问的模型路线、验证计划、图表证据和章节落点 |
| `paper_output/plan/rubric_alignment.json` | `modeling-paper-rubric-and-model-selector` | QA、微单元生成 | 保存评分点与证据形式的映射 |
| `paper_output/tasks.json` | `quality-assurance-auditor` | `paper-micro-unit-generator` | 保存微单元任务清单 |

## Rules

- 所有路径使用相对路径，不写入本机绝对路径。
- 所有 JSON 必须包含 `schema_version`、`generated_by`、`generated_at`。
- 子问题 ID 统一使用 `Q1`、`Q2`、`Q3`。
- JSON 只保存结构化交接信息，不保存完整论文正文。
- Markdown 用于解释为什么这样建模、如何对应评分点、后续生成应注意什么。
- 下游 skill 读取更具体的 contract 时，必须保留回退能力，避免缺少某个文件就中断全流程。

## Current Flow

```text
problem_files/
        ↓
problem-doc-model-selector
        ↓
paper_output/step1/problem_analysis.json
        ↓
modeling-paper-rubric-and-model-selector
        ↓
paper_output/plan/model_route.json
paper_output/plan/rubric_alignment.json
paper_output/plan/scoring_strategy.md
        ↓
quality-assurance-auditor
        ↓
paper_output/tasks.json
        ↓
paper-micro-unit-generator
        ↓
paper_output/final_paper.md
paper_output/final_paper.docx
```

## User Control

高级用户可以直接检查或修改 `paper_output/plan/model_route.json`。例如把某一问的 `main_model` 改成更合适的方法后，再重新运行 QA 和微单元生成，即可让后续正文围绕新的模型路线展开。

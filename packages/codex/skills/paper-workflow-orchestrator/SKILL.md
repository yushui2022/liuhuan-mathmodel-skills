---
name: "paper-workflow-orchestrator"
description: "串联赛题解析、数据计算与微单元脚本，一键从赛题文件夹到完整论文。Invoke when用户已放好赛题与附件，希望自动跑完全流程。"
---

# 论文生成全流程编排器

## 目标
- 串联现有技能与脚本，用尽量少的人工操作从赛题文件夹直接得到可提交的完整论文草稿。
- 保持本项目的核心思路：以 skill 为主线，把“赛题解析 → 模型选择 → 数据处理 → QA → 微单元生成 → 合并交付”串成一套可执行工作流。
- 注意：`scripts/run_all.py` 是离线一键样板入口，负责把已落地的脚本串起来；真正遇到新赛题时，Agent 仍应先读取 `problem-doc-model-selector`、`modeling-paper-rubric-and-model-selector` 和相关 `scripts/`，再按当前赛题二次生成或修改数据处理与建模代码。

## 自动化运行约定（Codex 中一键）
- **零交互原则 (Zero Interaction)**: 
  - 当用户给出赛题（或说“跑一下”、“生成论文”）时，**不要询问**“是否要生成？”、“是否需要清洗数据？”。
  - **立即**、**沉默**地启动 `run_all.py` 脚本。
  - 告诉用户：“正在全速生成中，预计耗时 20 分钟，请稍候...”，然后直接开始跑。
- 用户不需要手动运行任何脚本。
- 当用户在对话中要求“一键完成/自动跑完全流程”时，本技能应直接执行：
  - `python skills/paper-workflow-orchestrator/scripts/run_all.py`
  该脚本会按顺序执行：赛题结构化分析 → 模型路线与评分闭环 → 外部资源检查 → 数据与图表计划 → 数据清洗与可视化 → QA 动态任务清单 → 微单元离线生成 → 合并。

## 适用时机
- 用户已经在项目根目录下按约定放好了赛题 PDF/Word 和附件数据，需要“从零到万字论文”的一条龙自动流程时。
- 已经完成部分计算或占位符填充，但希望检查整体步骤是否完整、顺序是否合理，或想一键重跑核心流程时。

## 约束（必须遵守）

- **Memory Interaction (必做)**:
  - **全流程中**：作为总控，应当在每个关键步骤（清洗完、QA完、生成完）结束后，主动调用 `context-memory-keeper` 更新进度，确保如果流程中断，Memory 中留有断点记录。
- 本技能是全项目唯一“权威一键入口”。用户只要提出“生成完整论文/一键跑完”，优先执行本技能而不是让多个技能分散运行。
- 若 `problem_files/` 为空，必须先补齐赛题与附件数据，再运行流程。
- 若用户分开调用了其他技能，最终仍应回到本技能或按本技能的顺序完成：清洗与出图 → QA 任务清单 → 微单元生成 → 合并。

## 完整性交付标准（以此判断是否“论文生产完整”）

- **必须存在：`paper_output/final_paper.docx` (最终交付物，Word 格式)**
- 必须存在：`paper_output/final_paper.md` (中间 Markdown 稿)
- 必须存在：`paper_output/step1/problem_analysis.json`（结构化题意分析）
- 必须存在：`paper_output/plan/model_route.json`（模型路线契约）
- 必须存在：`paper_output/plan/rubric_alignment.json`（评分点映射契约）
- 必须存在：`paper_output/plan/data_plan.json` 与 `visualization_plan.json`（数据与图表证据链契约）
- 必须存在：`paper_output/figure_index.json`（图表计划索引）
- 必须存在：`paper_output/tasks.json`
- 必须存在：`paper_output/ref_check.md`
- 必须存在：`paper_output/micro_units/`（可允许少量单元缺失，但合并稿需能正常阅读）
- 建议存在：`paper_output/figures/` 与 `paper_output/data_cleaned/`（用于数据预处理与结果分析配图）

## 脚本清单（本技能实际会用到的）
- `scripts/run_all.py`：离线一键全流程入口。
  - 何时用：用户要求“一键完成/自动跑完全流程”。
  - 做什么：先跑 `problem-doc-model-selector/scripts/analyze_problem.py` 生成 `problem_analysis.json` → 再跑 `modeling-paper-rubric-and-model-selector/scripts/build_model_route.py` 生成模型路线与评分点契约 → 再生成数据/图表证据链契约并做清洗与可视化 → 再跑 QA 生成动态 `paper_output/tasks.json` → 再离线生成微单元 → 再合并成 `paper_output/final_paper.md` 和 `paper_output/final_paper.docx`。

## 前置约定
- 目录结构建议为：
  - 根目录：`<项目根目录>`
  - 赛题与附件：`problem_files/`（把赛题 PDF/Word 与附件数据直接放这里；QA 会检查该目录不为空）
  - 补充数据：`crawled_data/`（可选，爬虫或外部公开数据放这里）
  - 输出目录：`paper_output/`（脚本自动生成任务清单、微单元与合并稿）
  - 技能目录：`skills/...`
- Python 可用即可。

## 输入
- 必填：
  - 将赛题 PDF/Word 与附件数据放入 `problem_files/`。
- 可选：
  - 将补充数据放入 `crawled_data/`。

## 输出
- 中间文件：
  - `paper_output/step1/problem_analysis.json`：结构化赛题分析，连接后续 QA 与正文生成。
  - `paper_output/step1/A_题意对齐.md`、`B_论文大纲.md`、`C_评分点对齐表.md`、`D_模型路线.json`。
  - `paper_output/plan/model_route.json`：每一问的模型路线、验证计划和建议图表。
  - `paper_output/plan/rubric_alignment.json`：评分点与证据映射。
  - `paper_output/plan/scoring_strategy.md`：评分闭环说明。
  - `paper_output/plan/data_plan.json`：数据文件、字段画像、清洗任务与子问题链接。
  - `paper_output/plan/visualization_plan.json`：建议图表、图题、用途、候选字段与输出路径。
  - `paper_output/figure_index.json`：图表计划索引，供 QA 和正文引用核对。
  - `paper_output/tasks.json`：微单元任务清单。
  - `paper_output/micro_units/*.txt`：每个微单元一个文件。
  - `paper_output/generate_log.json`：生成日志。
- 最终交付：
  - `paper_output/final_paper.md`：合并后的论文草稿。
  - `paper_output/ref_check.md`：交叉引用与编号断链报告。

## 工作流程（对应 workflow_full 分步）

### 当前实现：离线一键流程（已落地）
1. **赛题结构化分析**:
   - 调用 `problem-doc-model-selector/scripts/analyze_problem.py`，生成 `paper_output/step1/problem_analysis.json`。
   - 将每一问的任务类型、推荐模型、验证计划和建议图表固化为后续 skill 可读取的数据契约。
2. **模型路线与评分闭环**:
   - 调用 `modeling-paper-rubric-and-model-selector/scripts/build_model_route.py`，生成 `paper_output/plan/model_route.json`、`rubric_alignment.json` 和 `scoring_strategy.md`。
   - 若该步骤失败，流程继续，QA 回退到 `problem_analysis.json`。
3. **外部资源获取 (Optional)**:
   - 调用 `authoritative-data-harvester` 或 `g-sci` (若存在) 填充 `crawled_data/`。
   - **Memory Update**: 将获取的文献/数据源更新至 `memoryskill.md`。
4. 调用 `data-cleaning-and-visualization/scripts/run_pipeline.py`：先生成 `data_plan.json`、`visualization_plan.json` 与 `figure_index.json`，再扫描 `problem_files/` 与 `crawled_data/`，产出清洗数据与图表到 `paper_output/`。
5. 调用 `quality-assurance-auditor/scripts/pipeline.py`：检查 `problem_files/`，优先根据 `model_route.json` 与 `rubric_alignment.json` 生成动态 `paper_output/tasks.json`。
6. 调用 `paper-micro-unit-generator/scripts/generate_all_offline.py`：生成 `paper_output/micro_units/*.txt` 与 `paper_output/generate_log.json`。
7. 调用 `paper-micro-unit-generator/scripts/merge.py`：生成 `paper_output/final_paper.md` 与 `paper_output/ref_check.md`，**并直接生成 `paper_output/final_paper.docx`**。
8. **[Mandatory] Word 交付验证**:
   - 检查 `paper_output/final_paper.docx` 是否存在。
   - 优先使用 `scripts/merge.py` 直接生成的 Word 版本（原生 python-docx 生成，不依赖 Pandoc）。
   - 仅在直接生成失败时，才尝试调用 Pandoc 作为兜底方案。
   - 确保公式、图表、目录在 Word 中显示正常。

### 分步运行（需要时才用）

0. **外部资源获取**:
   - 若需要补充文献或数据，先运行 `authoritative-data-harvester` 或其他搜索技能。

1. 仅做数据清洗与可视化：
```bash
python skills/data-cleaning-and-visualization/scripts/run_pipeline.py
```

2. 仅做赛题结构化分析：
```bash
python skills/problem-doc-model-selector/scripts/analyze_problem.py
```

3. 仅生成模型路线与评分闭环：
```bash
python skills/modeling-paper-rubric-and-model-selector/scripts/build_model_route.py
```

4. 仅生成任务清单（会检查 `problem_files/` 不为空，并优先读取 `model_route.json`）：
```bash
python skills/quality-assurance-auditor/scripts/pipeline.py
```

5. 仅生成微单元：
```bash
python skills/paper-micro-unit-generator/scripts/generate_all_offline.py
```

6. 仅合并生成论文：
```bash
python skills/paper-micro-unit-generator/scripts/merge.py
```

## 常见问题

- 报错“problem_files 为空”：把赛题 PDF/Word 与附件数据放进 `problem_files/` 后重跑。
- 想要看题意拆解：查看 `paper_output/step1/problem_analysis.json` 和 `paper_output/step1/A_题意对齐.md`。
- 想要看模型路线：查看 `paper_output/plan/model_route.json` 和 `paper_output/plan/scoring_strategy.md`。
- 想要看论文产出：最终文件是 `paper_output/final_paper.md`。
- 想要看数据与图表：清洗数据在 `paper_output/data_cleaned/`，图表在 `paper_output/figures/`。

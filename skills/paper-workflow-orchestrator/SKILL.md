---
name: "paper-workflow-orchestrator"
description: "串联赛题解析、数据计算与微单元脚本，一键从赛题文件夹到完整论文。Invoke when用户已放好赛题与附件，希望自动跑完全流程。"
---

# 论文生成全流程编排器

## 目标
- 串联现有技能与脚本，用尽量少的人工操作从赛题文件夹直接得到可提交的完整论文草稿。

## 自动化运行约定（Trae 内一键）
- 用户不需要手动运行任何脚本。
- 当用户在对话中要求“一键完成/自动跑完全流程”时，本技能应直接执行：
  - `python .trae/skills/paper-workflow-orchestrator/scripts/run_all.py`
  该脚本会按顺序执行：数据清洗与可视化 → QA 任务清单 → 微单元离线生成 → 合并。

## 适用时机
- 用户已经在项目根目录下按约定放好了赛题 PDF/Word 和附件数据，需要“从零到万字论文”的一条龙自动流程时。
- 已经完成部分计算或占位符填充，但希望检查整体步骤是否完整、顺序是否合理，或想一键重跑核心流程时。

## 约束（必须遵守）

- 本技能是全项目唯一“权威一键入口”。用户只要提出“生成完整论文/一键跑完”，优先执行本技能而不是让多个技能分散运行。
- 若 `problem_files/` 为空，必须先补齐赛题与附件数据，再运行流程。
- 若用户分开调用了其他技能，最终仍应回到本技能或按本技能的顺序完成：清洗与出图 → QA 任务清单 → 微单元生成 → 合并。

## 完整性交付标准（以此判断是否“论文生产完整”）

- 必须存在：`paper_output/final_paper.md`
- 必须存在：`paper_output/tasks.json`
- 必须存在：`paper_output/ref_check.md`
- 必须存在：`paper_output/micro_units/`（可允许少量单元缺失，但合并稿需能正常阅读）
- 建议存在：`paper_output/figures/` 与 `paper_output/data_cleaned/`（用于数据预处理与结果分析配图）

## 脚本清单（本技能实际会用到的）
- `scripts/run_all.py`：离线一键全流程入口。
  - 何时用：用户要求“一键完成/自动跑完全流程”。
  - 做什么：先做数据清洗与可视化 → 再跑 QA 生成 `paper_output/tasks.json` → 再离线生成微单元 → 再合并成 `paper_output/final_paper.md`。

## 前置约定
- 目录结构建议为：
  - 根目录：`c:\Users\xiaoy\Desktop\trae\数学建模`
  - 赛题与附件：`problem_files/`（把赛题 PDF/Word 与附件数据直接放这里；QA 会检查该目录不为空）
  - 补充数据：`crawled_data/`（可选，爬虫或外部公开数据放这里）
  - 输出目录：`paper_output/`（脚本自动生成任务清单、微单元与合并稿）
  - 技能目录：`.trae/skills/...`
- Python 可用即可。

## 输入
- 必填：
  - 将赛题 PDF/Word 与附件数据放入 `problem_files/`。
- 可选：
  - 将补充数据放入 `crawled_data/`。

## 输出
- 中间文件：
  - `paper_output/tasks.json`：微单元任务清单。
  - `paper_output/micro_units/*.txt`：每个微单元一个文件。
  - `paper_output/generate_log.json`：生成日志。
- 最终交付：
  - `paper_output/final_paper.md`：合并后的论文草稿。
  - `paper_output/ref_check.md`：交叉引用与编号断链报告。

## 工作流程（对应 workflow_full 分步）

### 当前实现：离线一键流程（已落地）
1. 调用 `data-cleaning-and-visualization/scripts/run_pipeline.py`：扫描 `problem_files/` 与 `crawled_data/`，产出清洗数据与图表到 `paper_output/`。
2. 调用 `quality-assurance-auditor/scripts/pipeline.py`：检查 `problem_files/`，生成 `paper_output/tasks.json`。
3. 调用 `paper-micro-unit-generator/scripts/generate_all_offline.py`：生成 `paper_output/micro_units/*.txt` 与 `paper_output/generate_log.json`。
4. 调用 `paper-micro-unit-generator/scripts/merge.py`：生成 `paper_output/final_paper.md` 与 `paper_output/ref_check.md`。

### 分步运行（需要时才用）

1. 仅做数据清洗与可视化：
```bash
python .trae/skills/data-cleaning-and-visualization/scripts/run_pipeline.py
```

2. 仅生成任务清单（会检查 `problem_files/` 不为空）：
```bash
python .trae/skills/quality-assurance-auditor/scripts/pipeline.py
```

3. 仅生成微单元：
```bash
python .trae/skills/paper-micro-unit-generator/scripts/generate_all_offline.py
```

4. 仅合并生成论文：
```bash
python .trae/skills/paper-micro-unit-generator/scripts/merge.py
```

## 常见问题

- 报错“problem_files 为空”：把赛题 PDF/Word 与附件数据放进 `problem_files/` 后重跑。
- 想要看论文产出：最终文件是 `paper_output/final_paper.md`。
- 想要看数据与图表：清洗数据在 `paper_output/data_cleaned/`，图表在 `paper_output/figures/`。

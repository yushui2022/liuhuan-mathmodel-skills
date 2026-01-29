# 数学建模论文自动化流水线（Trae Skills）

本项目把“赛题解析 → 数据整理 → 写作生成 → 合并成稿”固化为一条可复用的流水线。你只需要把赛题与附件按约定放好，然后一键运行，即可在 `paper_output/` 下拿到论文草稿与支撑图表。

## 快速开始（推荐）

1. 把赛题 PDF/Word 与附件数据放进：`problem_files/`
2. （可选）把爬虫/外部补充数据放进：`crawled_data/`
3. 在项目根目录运行：

```bash
python .trae/skills/paper-workflow-orchestrator/scripts/run_all.py
```

最终交付在：`paper_output/final_paper.md`

## 目录约定（统一口径）

为避免“skills 各自为战”，本项目把输入输出目录统一成三类：

```text
数学建模/
├── problem_files/                 # 输入：赛题 PDF/Word + 官方附件数据（必填）
├── crawled_data/                  # 输入：补充/爬虫/权威数据（可选）
├── paper_output/                  # 输出：一切中间产物与最终论文（自动生成）
│   ├── tasks.json                 # 任务清单（微单元）
│   ├── micro_units/               # 微单元文本（逐条生成）
│   ├── generate_log.json          # 生成日志
│   ├── final_paper.md             # 最终合并稿（核心交付）
│   ├── ref_check.md               # 引用/编号断链报告
│   ├── data_cleaned/              # 清洗后的数据
│   └── figures/                   # 图表（可直接插入论文）
└── .trae/skills/                  # 技能定义与脚本
```

约束：
- `problem_files/` 必须非空，否则 QA 会阻塞后续流程。
- 任何脚本或技能生成的中间文件，统一归档到 `paper_output/`，避免散落在根目录。

## 一键流程的运行轨迹

一键入口：`paper-workflow-orchestrator` 会按固定顺序串联以下步骤（对应脚本见 [run_all.py](file:///c:/Users/xiaoy/Desktop/trae/数学建模/.trae/skills/paper-workflow-orchestrator/scripts/run_all.py)）：

1. 数据清洗与可视化：`data-cleaning-and-visualization`
   - 输入：`problem_files/`、`crawled_data/`
   - 输出：`paper_output/data_cleaned/`、`paper_output/figures/`
2. 质量门禁与任务清单：`quality-assurance-auditor`
   - 输入：检查 `problem_files/` 非空
   - 输出：`paper_output/tasks.json`、初始化 `paper_output/micro_units/`
3. 微单元离线生成：`paper-micro-unit-generator`
   - 输入：`paper_output/tasks.json`
   - 输出：`paper_output/micro_units/*.txt`、`paper_output/generate_log.json`
4. 合并成稿：`paper-micro-unit-generator`
   - 输入：`paper_output/micro_units/*.txt`
   - 输出：`paper_output/final_paper.md`、`paper_output/ref_check.md`

## Skills 总览与推荐顺序

下面给出“规划类 → 数据类 → 产文类 → 全局监督”的推荐顺序。你也可以直接跳到“一键流程”。

### A. 规划类（先把题意与评分点对齐）

- `modeling-paper-rubric-and-model-selector`
  - 作用：生成论文结构/评分点清单/模型路线（基线-改进-验证）。
  - 建议归档：`paper_output/plan/`。
  - 后续接：`problem-doc-model-selector` 或直接一键流程。

- `problem-doc-model-selector`
  - 作用：解析赛题 PDF/Word，逐问抽取任务/约束/数据条件并给出模型路线。
  - 建议归档：`paper_output/step1/`。
  - 后续接：数据获取/数据清洗，或直接一键流程。

### B. 数据类（把数据准备到可用状态）

- `authoritative-data-harvester`
  - 作用：补充权威公开数据，输出可复现抓取方案。
  - 归档约定：`crawled_data/raw/`、`crawled_data/processed/`、`crawled_data/sources.json`。
  - 后续接：`data-cleaning-and-visualization`。

- `data-cleaning-and-visualization`
  - 作用：清洗 `problem_files/` 与 `crawled_data/` 里的结构化数据，生成 EDA 图表。
  - 产物：`paper_output/data_cleaned/`、`paper_output/figures/`。
  - 后续接：`quality-assurance-auditor`。

### C. 产文类（把结构变成完整论文文本）

- `paper-structured-composer`
  - 作用：章节/小节级别的分解生成与合并，适合“需要补写某几个章节”或“先有一个可读的大纲版正文”。
  - 建议归档：`paper_output/structured_sections/` 与 `paper_output/structured_paper.md`。
  - 后续接：`quality-assurance-auditor` 或 `paper-micro-unit-generator`。

- `paper-micro-unit-generator`
  - 作用：微单元级别批量生成与合并（更细粒度、更容易控字数与覆盖评分点）。
  - 产物：`paper_output/micro_units/`、`paper_output/final_paper.md`。
  - 前置依赖：`quality-assurance-auditor` 先生成 `paper_output/tasks.json`。

### D. 全局监督（建议每个阶段都用）

- `quality-assurance-auditor`
  - 作用：全局门禁与一致性检查（目录必检、任务清单生成、合并前后把关）。
  - 一句话：没过它就不进入下一步。

## 常见问题

- “数据到底放哪？”：官方附件放 `problem_files/`，补充数据放 `crawled_data/`。
- “文章在哪里？”：看 `paper_output/final_paper.md`。
- “为什么有的 skill 文档写的路径不一致？”：已统一以本 README 的三大目录为准；各 skill 的 `SKILL.md` 已补充“目录约定/前后衔接”。

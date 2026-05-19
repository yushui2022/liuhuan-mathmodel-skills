<div align="center">
  <img src="./assets/mathe-skill-logo.svg" alt="MathModel Skill logo" width="132" height="132" />

# MathModel Skill

### 数学建模论文自动化多 Agent 原生 Skill 流程

#### 为 Trae、Claude Code、Codex 设计的完整数学建模 Skill 包

[![Core Skills](https://img.shields.io/badge/core%20skills-7-2563eb)](#四部分七个核心-skills)
[![Trae](https://img.shields.io/badge/Trae-native-0ea5e9)](#选择你的-agent-平台)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-native-7c3aed)](#选择你的-agent-平台)
[![Codex](https://img.shields.io/badge/Codex-native-111827)](#选择你的-agent-平台)
[![Workflow](https://img.shields.io/badge/workflow-one--click-0ea5e9)](#30-秒上手)
[![Output](https://img.shields.io/badge/output-docx%20%2B%20markdown-16a34a)](#项目目录约定)

</div>

这套项目把数学建模比赛里最容易卡人的流程拆成一组可复用的 skills：

```text
赛题解析 -> 模型选择 -> 数据获取 -> 数据清洗与可视化 -> 论文微单元生成 -> 质量审计 -> 合并成稿
```

你可以把它理解成一个“数学建模论文生产流水线”。用户只需要把赛题 PDF/Word 和附件数据放到指定文件夹，然后说“开始生成”或直接运行一键脚本，系统会按固定顺序完成清洗、出图、任务拆分、正文生成、合并和 Word 导出。

本仓库按完整 skill 包分发，不把 skill 压平成单个 Markdown 文件。每个 skill 都保留自己的 `SKILL.md`、`scripts/`、`references/`、memory 文件等资源。

本 README 主要面向两类人：

- 想直接使用这套 skills 跑数学建模题的人。
- 想学习如何搭建一套自己的多 skill 工作流的人。

## 选择你的 Agent 平台

这套项目不是只给 Trae 用。Trae、Claude Code、Codex 都有自己的原生 skill 包：

| 你使用的工具 | 下载/复制这个目录 | 复制到你的项目里 | 说明 |
|---|---|---|---|
| Trae | `trae/.trae/skills/` | `.trae/skills/` | 当前最成熟原版 skill 包 |
| Claude Code | `claude/.claude/skills/` + `claude/CLAUDE.md` | `.claude/skills/` + `CLAUDE.md` | Claude Code 原生 skill 包 |
| Codex | `codex/skills/` + `codex/AGENTS.md` | `skills/` + `AGENTS.md` | Codex 原生 skill 包 |

详细安装方式见 [Agent 安装指南](docs/agent-install-guide.md)。

## 30 秒上手

如果你只想在当前仓库先跑起来，按下面三步做：

1. 把赛题 PDF/Word 和官方附件数据放进项目根目录下的 `problem_files/`。
2. 可选：把外部补充数据、爬虫数据、统计表放进 `crawled_data/`。
3. 在项目根目录运行：

```bash
python .trae/skills/paper-workflow-orchestrator/scripts/run_all.py
```

运行结束后，主要看这几个文件：

```text
paper_output/final_paper.docx      # 最终 Word 论文
paper_output/final_paper.md        # Markdown 合并稿
paper_output/tasks.json            # 论文微单元任务清单
paper_output/ref_check.md          # 图表/公式/引用断链检查
paper_output/data_cleaned/         # 清洗后的数据
paper_output/figures/              # 自动生成的图表
```

如果你在 Windows PowerShell 里遇到 `UnicodeEncodeError: 'gbk' codec can't encode...`，先执行：

```powershell
$env:PYTHONIOENCODING="utf-8"
python .trae/skills/paper-workflow-orchestrator/scripts/run_all.py
```

## 项目目录约定

所有 skills 都围绕这三个核心目录工作，建议不要改名：

```text
liuhuan-mathmodel-skills/
├── trae/                         # Trae 原生 skill 包
├── claude/                       # Claude Code 原生 skill 包
├── codex/                        # Codex 原生 skill 包
├── docs/                         # 安装说明与平台说明
├── problem_files/                 # 输入：赛题 PDF/Word + 官方附件数据
├── crawled_data/                  # 输入：外部补充数据、权威数据、爬虫数据
├── paper_output/                  # 输出：中间产物、图表、最终论文
│   ├── tasks.json                 # 微单元任务清单
│   ├── micro_units/               # 每个论文微单元的文本
│   ├── generate_log.json          # 微单元生成日志
│   ├── final_paper.md             # Markdown 合并稿
│   ├── final_paper.docx           # Word 最终稿
│   ├── ref_check.md               # 引用/图表/公式断链检查
│   ├── data_cleaned/              # 清洗后的结构化数据
│   └── figures/                   # 可插入论文的图表
└── .trae/skills/                  # Trae 原版 canonical skill source
```

约束很简单：

- `problem_files/` 必须非空，否则质量审计会阻塞后续流程。
- 原始数据不要直接改，清洗结果统一写入 `paper_output/data_cleaned/`。
- 论文里要用的图表统一从 `paper_output/figures/` 引用。
- 最终交付以 `paper_output/final_paper.docx` 为准，`final_paper.md` 作为可读中间稿。

## 四部分，七个核心 Skills

这套流程的核心是 7 个 skills。另有一个 `context-memory-keeper` 用来记录流程状态和长期约束，属于辅助记忆 skill。

### 第一部分：正文模型选择与逻辑闭环

#### `problem-doc-model-selector`

作用：读取赛题 PDF/Word 或题面文本，自动拆解每一问要解决什么问题。

它重点回答：

- 每一问的输入是什么？
- 输出结果应该是什么？
- 这是预测、优化、分类、评价、聚类还是仿真问题？
- 题目有哪些显式约束、单位口径和数据条件？
- 每问适合用什么基线模型和改进模型？

典型使用场景：

```text
我把赛题放到 problem_files/ 了，请解析题目并判断每一问适合用什么模型。
```

#### `modeling-paper-rubric-and-model-selector`

作用：把模型路线和竞赛论文评分点对齐，补全“为什么这样建模、这样写能拿分”的逻辑。

它重点输出：

- 一页纸题意对齐。
- 评分点 -> 证据 -> 论文位置 的映射表。
- 论文大纲。
- 每问的基线模型、改进路线、验证计划和风险。

它不是单纯帮你“想模型”，而是让模型选择能落到论文结构、图表证据和评分点上。

### 第二部分：数据获取、清洗与可视化

#### `authoritative-data-harvester`

作用：在题目需要外部数据时，帮助定位权威公开数据源。

优先级：

```text
官方 API -> 官方批量下载 -> 网页表格 -> 手动搜索提示
```

推荐放置位置：

```text
crawled_data/raw/          # 原始下载文件
crawled_data/processed/    # 处理后的结构化数据
crawled_data/sources.json  # 数据来源、链接、访问日期、许可证说明
```

#### `data-cleaning-and-visualization`

作用：扫描 `problem_files/` 和 `crawled_data/` 中的 CSV、Excel、TXT 数据，自动做基础清洗和可视化。

当前脚本会做：

- 读取 `.csv`、`.xlsx`、`.xls`、`.txt`。
- 删除全空行、全空列。
- 自动尝试把文本列转成数值列。
- 数值缺失值用均值填补。
- 分类缺失值用众数填补。
- 去重。
- 生成分布图、相关性热力图、散点矩阵、分类柱状图。

单独运行：

```bash
python .trae/skills/data-cleaning-and-visualization/scripts/run_pipeline.py
```

### 第三部分：整体论文生成与质量审计

#### `paper-micro-unit-generator`

作用：把整篇论文拆成多个微单元，每个单元单独生成，最后再合并成完整论文。

这个设计解决的是一个常见问题：让模型一次性写完整篇论文，容易漏问题、漏约束、结构混乱、前后不一致。拆成微单元之后，每个小块都有明确职责，后续也更容易检查和重跑。

它主要依赖两个脚本：

```bash
python .trae/skills/paper-micro-unit-generator/scripts/generate_all_offline.py
python .trae/skills/paper-micro-unit-generator/scripts/merge.py
```

输入：

```text
paper_output/tasks.json
```

输出：

```text
paper_output/micro_units/*.txt
paper_output/generate_log.json
paper_output/final_paper.md
paper_output/final_paper.docx
paper_output/ref_check.md
```

#### `quality-assurance-auditor`

作用：作为全局质量门禁，检查目录、任务清单、微单元进度和最终产物是否满足继续往下走的条件。

它应该承担的职责包括：

- 检查 `problem_files/` 是否有赛题或附件。
- 生成 `paper_output/tasks.json`。
- 检查微单元是否缺失。
- 检查正文是否还有占位符。
- 检查图表、公式、引用是否断链。
- 检查每一问是否都有模型、结果、验证和结论。

单独运行：

```bash
python .trae/skills/quality-assurance-auditor/scripts/pipeline.py
```

### 第四部分：中心编排器

#### `paper-workflow-orchestrator`

作用：管理全局执行顺序，避免用户或模型忘记下一步该干什么。

一键入口：

```bash
python .trae/skills/paper-workflow-orchestrator/scripts/run_all.py
```

当前执行顺序：

```text
1. 尝试读取/执行外部数据需求
2. 数据清洗与可视化
3. 可选执行自定义计算脚本 step2_calc_results.py
4. 质量审计，生成 tasks.json
5. 批量生成微单元
6. 合并 Markdown
7. 导出 Word
```

用户在对话里说下面这些话时，都应该优先走这个 skill：

```text
开始生成
跑一下这个题
一键生成论文
从赛题到论文跑完整流程
把这个数学建模题做完并生成 Word
```

## 辅助 Skill：记忆管理

#### `context-memory-keeper`

作用：记录长期规则和当前任务状态，避免流程跑到一半丢上下文。

核心文件：

```text
.trae/skills/context-memory-keeper/memoryskill.md
.trae/skills/context-memory-keeper/memory_archive.md
```

它适合记录：

- 当前赛题的核心任务。
- 用户偏好的论文风格。
- 已经获取的数据源。
- 当前流程执行到哪一步。
- 哪些问题还没解决。

如果你要继续升级这套项目，建议保留这个 skill。它不属于论文生产主流程，但对长任务非常有用。

## 推荐使用流程

### 第 1 步：准备项目

克隆仓库：

```bash
git clone https://github.com/yushui2022/liuhuan-mathmodel-skills.git
cd liuhuan-mathmodel-skills
```

建议准备 Python 环境，并安装常用依赖：

```bash
pip install pandas numpy matplotlib seaborn requests python-docx openpyxl
```

### 第 2 步：放入赛题和附件

把赛题 PDF/Word、附件 Excel、CSV 等全部放进：

```text
problem_files/
```

如果题目需要外部统计数据，把你已有的数据放进：

```text
crawled_data/
```

### 第 3 步：一键运行

```bash
python .trae/skills/paper-workflow-orchestrator/scripts/run_all.py
```

### 第 4 步：检查输出

优先检查：

```text
paper_output/final_paper.docx
paper_output/ref_check.md
paper_output/figures/
paper_output/generate_log.json
```

如果 `ref_check.md` 提示断链，说明正文引用了不存在的图、表或公式，需要修正对应微单元后重新合并。

### 第 5 步：局部重跑

如果只想重新清洗数据：

```bash
python .trae/skills/data-cleaning-and-visualization/scripts/run_pipeline.py
```

如果只想重新生成任务清单：

```bash
python .trae/skills/quality-assurance-auditor/scripts/pipeline.py
```

如果只想重新生成正文微单元：

```bash
python .trae/skills/paper-micro-unit-generator/scripts/generate_all_offline.py
```

如果只想重新合并 Word：

```bash
python .trae/skills/paper-micro-unit-generator/scripts/merge.py
```

## 常用对话指令

在支持 skills 的对话环境里，可以直接这样说：

```text
我把赛题放好了，开始生成。
```

```text
先解析这个赛题，告诉我每一问适合用什么模型。
```

```text
把附件数据清洗一下，并生成论文可用的图表。
```

```text
检查一下当前论文有没有漏问题、图表断链或占位符。
```

```text
只重跑微单元生成和合并，不要重新清洗数据。
```

## 如何制作自己的 Skill 流程

这套项目的核心方法不是某一个提示词，而是“把复杂任务拆成多个职责稳定的 skill，再用中心编排器串起来”。

你可以按下面方式复刻：

1. 先拆流程，而不是先写 prompt。
   例如数学建模可以拆成：读题、选模型、找数据、清洗、画图、写论文、审计、合并。

2. 每个 skill 只负责一个清晰任务。
   不要让一个 skill 同时做读题、写论文、画图和审计，否则后续很难维护。

3. 给每个 skill 固定输入输出目录。
   例如数据永远从 `problem_files/` 和 `crawled_data/` 读，产物永远写到 `paper_output/`。

4. 能脚本化的部分尽量脚本化。
   清洗数据、生成图表、合并文件、检查断链这些工作适合写成 Python 脚本，减少模型临场发挥。

5. 必须有全局门禁。
   论文生成前检查题目是否存在，合并前检查微单元是否齐全，交付前检查 Word 是否生成。

6. 最后才写中心编排器。
   编排器只负责顺序，不负责具体业务。这样后续替换某个 skill 时，不会影响整条流水线。

## 当前版本的现实边界

这个仓库已经具备完整流水线骨架，也能通过脚本生成基础论文产物。但如果你要把它用于真实高强度比赛，还建议继续增强：

- 把 `problem-doc-model-selector` 的解析结果结构化落盘，供后续脚本读取。
- 把 `tasks.json` 从固定章节扩展为根据赛题动态生成。
- 把微单元数量扩展到更细粒度，并为每个单元配置字数、关键词、证据来源和 QA 规则。
- 强化 `quality-assurance-auditor`，让它真正检查子问题覆盖、占位符、重复段落、图表断链和字数完成度。
- 增加更贴近论文的图表模板，例如模型对比图、敏感性分析图、误差分析图、结果汇总表。
- 给 Windows 终端输出做兼容，避免 GBK 编码环境下打印特殊字符失败。

## 常见问题

### 1. 报错 `problem_files 为空` 怎么办？

把赛题 PDF/Word 和附件数据放进 `problem_files/`，然后重新运行：

```bash
python .trae/skills/paper-workflow-orchestrator/scripts/run_all.py
```

### 2. 最终论文在哪里？

看：

```text
paper_output/final_paper.docx
paper_output/final_paper.md
```

### 3. 图表在哪里？

看：

```text
paper_output/figures/
```

### 4. 数据清洗后的文件在哪里？

看：

```text
paper_output/data_cleaned/
```

### 5. 为什么有些地方还是占位内容？

说明当前微单元没有拿到足够的赛题解析、模型结果或占位符数据。可以补充：

```text
step3_filled_placeholder.py
paper_output/step1/
paper_output/plan/
step2_calc_results.py
```

然后重新运行微单元生成和合并。

### 6. 为什么 Word 里的公式还是 LaTeX 源码？

当前 Word 导出优先使用 `python-docx` 直接生成，不依赖 Pandoc。这样更容易跑通，但复杂数学公式会以 LaTeX 源码形式保留。若要更高质量的公式排版，可以后续接入 Pandoc、MathType 或专门的公式转换模块。

## 一句话总结

这套 skills 的价值不在于“一个提示词写完整篇论文”，而在于把数学建模比赛拆成可控、可检查、可重跑的流水线：先理解题，再选模型，再处理数据，再分块写作，最后审计并合并交付。

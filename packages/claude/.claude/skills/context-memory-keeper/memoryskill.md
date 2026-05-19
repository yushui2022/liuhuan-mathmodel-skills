# Context Memory (Active)

> **Instructions for AI**: 
> 1. 读取此文件以恢复上下文。
> 2. **长期准则**仅在用户明确更改要求时修改。
> 3. **短期工作台**应随任务进展高频更新。
> 4. 当短期任务完成时，执行 **[归档操作]**：将旧条目移至 `memory_archive.md`，并将关键结论提炼回本文件的“长期准则”或保留在“项目状态”中。

## 0. 自动压缩规则 (Auto-Cleanup Rules)
> **Trigger**: 行数 > 100 行。
> **Keep**: 
> 1. 用户强指令 (Imperatives) & 核心需求 (Requirements)。
> 2. 项目骨架 (Framework) & 关键产物路径。
> **Archive**: 细节日志 -> `memory_archive.md`。

## 1. 长期准则 (Long-term Principles)
> **不可变/低频更新**：项目核心设定、用户偏好、全局约束。

- **Role**: 数学建模专家 (Expert in Mathematical Modeling)。
- **Structure Constitution (结构参考)**: 
  - 参考 `modeling-paper-rubric-and-model-selector/references/paper_prompt_default.md`。
  - **允许**学术性“车轱辘话”以增加体量；**严禁**机械式复制粘贴（如连续重复段落）。
  - **交付格式**: **必须包含 Word 文档 (.docx)**，严禁只交付 Markdown。
- **Output**: 
  - 语言：中文 (学术风格)。
  - 格式：标准竞赛论文结构 (问题重述、假设、建模、求解、分析、评价)。
- **Core Constraints**:
  - **Code**: 优先复用 `skills/` 下的现有脚本，避免重复造轮子。
  - **Quality**: 始终平衡理论严谨性与实际应用价值；主动解释复杂数学概念。
- **Project Goal**: 完成从赛题解析到论文生成的全流程自动化。

## 2. 短期工作台 (Short-term Workbench)
> **高频更新**：当前聚焦的任务、临时的上下文、待解决的 blocker。

- **Current Focus**: [优化记忆机制]
  - 用户要求将记忆拆分为“长期”与“短期”，并引入归档机制。
- **Active Context**:
  - 已创建 `context-memory-keeper` skill。
  - 正在重构文件结构。
- **External Resources / Literature (New)**:
  - [待更新]: 记录从 g-sci/authoritative-data-harvester 获取的关键文献或数据源。
- **Immediate Todos**:
  - [ ] 验证新结构的有效性。
  - [ ] 准备开始解析具体的赛题 (等待用户输入)。

## 3. 项目里程碑 (Milestones)
> 记录已完成的关键节点与产物路径。

- [x] Skill `context-memory-keeper` 初始化完成。

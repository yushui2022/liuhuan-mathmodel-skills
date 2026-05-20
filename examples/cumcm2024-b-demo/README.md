# CUMCM 2024 B Demo

本目录是 MathModel Skill 按 Agent-native 正式流程生成的 CUMCM 2024 B 题展示样例。

注意：仓库不包含官方 `B题.pdf`。用户如需复现完整流程，应自行从官方渠道准备赛题文件，并放入自己的 `problem_files/` 目录。

## 样例内容

```text
paper_output/
├── final_paper_source.md          # 正式论文 Markdown 源稿
├── final_paper.docx               # 由 paper-formal-writer 生成的正式 Word
├── format_check_report.md         # 正式格式门禁报告
├── qa/evidence_gate_report.md     # 证据门禁报告
├── plan/paper_outline.json        # 正式论文大纲契约
├── results/                       # 模型结果、指标和结论
├── tables/                        # 论文表格和 table_index.json
├── figures/                       # 论文图片
└── code/                          # 当前赛题专用建模代码
```

## 复核方式

在本目录运行对应平台的 skill 脚本，或从仓库根目录指定脚本路径并把工作目录设为本目录：

```bash
python skills/quality-assurance-auditor/scripts/evidence_gate.py
python skills/paper-formal-writer/scripts/build_paper_outline.py
python skills/paper-formal-writer/scripts/format_formal_docx.py
python skills/paper-formal-writer/scripts/check_paper_format.py
```

本样例用于展示新范式：证据链先产出真实结果、图表和表格，再由 `paper-formal-writer` 约束正式论文结构、标题编号、Word 排版和格式检查。它不是把官方赛题 PDF 打包进仓库的可复现原始数据集。

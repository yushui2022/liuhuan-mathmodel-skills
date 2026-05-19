import json
import os
import sys
from pathlib import Path


BASE_DIR = Path.cwd()
PROBLEM_DIR = BASE_DIR / "problem_files"
OUTPUT_DIR = BASE_DIR / "paper_output"
MICRO_UNITS_DIR = OUTPUT_DIR / "micro_units"
TASKS_FILE = OUTPUT_DIR / "tasks.json"
PROBLEM_ANALYSIS_FILE = OUTPUT_DIR / "step1" / "problem_analysis.json"


def init_project() -> None:
    for d in (PROBLEM_DIR, OUTPUT_DIR, MICRO_UNITS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def has_problem_files() -> bool:
    if not PROBLEM_DIR.exists():
        return False
    return any(PROBLEM_DIR.iterdir())


def load_existing_tasks() -> list[dict] | None:
    if not TASKS_FILE.exists():
        return None
    try:
        tasks = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
        return tasks if isinstance(tasks, list) else None
    except Exception:
        return None


def load_problem_analysis() -> dict | None:
    if not PROBLEM_ANALYSIS_FILE.exists():
        return None
    try:
        data = json.loads(PROBLEM_ANALYSIS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def question_section_name(index: int, question: dict) -> str:
    title = str(question.get("title") or "").strip()
    if title:
        return title
    numerals = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    suffix = numerals[index - 1] if 0 < index <= len(numerals) else str(index)
    return f"问题{suffix}"


def add_task(tasks: list[dict], task_id: str, section: str, target_words: int, **extra: object) -> None:
    payload = {
        "id": task_id,
        "section": section,
        "status": "pending",
        "target_words": int(target_words),
        "file_path": str(MICRO_UNITS_DIR / f"{task_id}.txt"),
    }
    payload.update(extra)
    tasks.append(payload)


def generate_dynamic_manifest(analysis: dict, target_words: int) -> list[dict]:
    questions = analysis.get("questions")
    if not isinstance(questions, list) or not questions:
        questions = []

    tasks: list[dict] = []
    add_task(tasks, "ABS-1", "摘要", target_words, role="background_and_problem")
    add_task(tasks, "ABS-2", "摘要", target_words, role="methods_overview")
    add_task(tasks, "ABS-3", "摘要", target_words, role="results_overview")
    add_task(tasks, "ABS-4", "摘要", target_words, role="validation_and_value")
    add_task(tasks, "ABS-5", "摘要", 120, role="keywords")

    add_task(tasks, "INTRO-1", "问题重述", target_words, role="background")
    add_task(tasks, "INTRO-2", "问题重述", target_words, role="question_breakdown")
    add_task(tasks, "INTRO-3", "问题重述", target_words, role="computable_tasks")

    add_task(tasks, "ASSUMP-1", "模型假设", target_words, role="assumptions")
    add_task(tasks, "ASSUMP-2", "模型假设", target_words, role="assumption_rationale")
    add_task(tasks, "SYMBOL-1", "符号说明", target_words, role="symbol_table")

    data_files = analysis.get("data_files") if isinstance(analysis.get("data_files"), list) else []
    data_units = max(3, min(5, len(data_files) + 2))
    for i in range(1, data_units + 1):
        add_task(tasks, f"DATA-{i}", "数据预处理", target_words, role="data_processing", data_file_count=len(data_files))

    if not questions:
        questions = [
            {
                "id": "Q1",
                "title": "问题一",
                "task_type": "综合建模/统计分析",
                "recommended_models": {"baseline": "可解释基线模型", "improved": "结合题目需求的改进模型"},
                "validation_plan": ["结果复核", "敏感性分析"],
                "figure_suggestions": ["数据概览图", "结果对比图"],
            }
        ]

    for index, question in enumerate(questions, start=1):
        section = question_section_name(index, question)
        qid = str(question.get("id") or f"Q{index}")
        model = question.get("recommended_models") if isinstance(question.get("recommended_models"), dict) else {}
        metadata = {
            "question_id": qid,
            "task_type": question.get("task_type", "综合建模/统计分析"),
            "baseline_model": model.get("baseline", "可解释基线模型"),
            "improved_model": model.get("improved", "结合题目需求的改进模型"),
            "validation_plan": question.get("validation_plan", []),
            "figure_suggestions": question.get("figure_suggestions", []),
        }
        roles = [
            "task_definition",
            "model_rationale",
            "model_formulation",
            "algorithm_design",
            "result_presentation",
            "validation",
            "sensitivity",
            "question_conclusion",
        ]
        for unit_index, role in enumerate(roles, start=1):
            add_task(tasks, f"{qid}-{unit_index}", section, target_words, role=role, **metadata)

    analysis_units = max(3, min(6, len(questions) + 2))
    for i in range(1, analysis_units + 1):
        add_task(tasks, f"ANALYSIS-{i}", "结果分析", target_words, role="result_analysis")

    add_task(tasks, "EVAL-1", "模型评价", target_words, role="advantages")
    add_task(tasks, "EVAL-2", "模型评价", target_words, role="limitations")
    add_task(tasks, "EVAL-3", "模型评价", target_words, role="extension")

    conclusion_units = max(2, min(4, len(questions) + 1))
    for i in range(1, conclusion_units + 1):
        add_task(tasks, f"CONCL-{i}", "结论", target_words, role="conclusion")

    add_task(tasks, "REF-1", "参考文献", 160, role="references")
    add_task(tasks, "APP-1", "附录", target_words, role="reproducibility")
    add_task(tasks, "APP-2", "附录", target_words, role="code_and_paths")
    return tasks


def generate_task_manifest(target_words: int = 300, force: bool = False) -> tuple[list[dict], bool]:
    existing = load_existing_tasks()
    if existing is not None and not force:
        return existing, False

    analysis = load_problem_analysis()
    if analysis is not None:
        tasks = generate_dynamic_manifest(analysis, target_words)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        TASKS_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
        return tasks, True

    sections = [
        ("ABS", "摘要", 5),
        ("INTRO", "问题重述", 3),
        ("ASSUMP", "模型假设", 2),
        ("SYMBOL", "符号说明", 1),
        ("DATA", "数据预处理", 4),
        ("MODEL1", "问题一", 8),
        ("MODEL2", "问题二", 8),
        ("MODEL3", "问题三", 8),
        ("ANALYSIS", "结果分析", 5),
        ("EVAL", "模型评价", 3),
        ("CONCL", "结论", 2),
        ("REF", "参考文献", 1),
        ("APP", "附录", 2),
    ]

    tasks: list[dict] = []
    for sec_code, sec_name, unit_count in sections:
        for i in range(1, unit_count + 1):
            task_id = f"{sec_code}-{i}"
            tasks.append(
                {
                    "id": task_id,
                    "section": sec_name,
                    "status": "pending",
                    "target_words": int(target_words),
                    "file_path": str(MICRO_UNITS_DIR / f"{task_id}.txt"),
                }
            )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TASKS_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
    return tasks, True


def audit_gate(stage_name: str) -> bool:
    if stage_name == "赛题目录检查":
        if not has_problem_files():
            print(f"❌ 审计未通过：{PROBLEM_DIR} 为空")
            print("🔒 请先把赛题 PDF/Word 和附件数据放进 problem_files/ 再继续")
            return False

    return True


def verify_completeness() -> tuple[int, int, int]:
    if not TASKS_FILE.exists():
        return 0, 0, 0

    tasks = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    total = len(tasks)
    ok = 0
    total_chars = 0

    for t in tasks:
        p = Path(t["file_path"])
        if not p.exists():
            continue
        content = p.read_text(encoding="utf-8")
        total_chars += len(content)
        if len(content) >= int(t.get("target_words", 0)):
            ok += 1

    return ok, total, total_chars


def scan_generated_text() -> list[str]:
    warnings: list[str] = []
    targets = []
    if (OUTPUT_DIR / "final_paper.md").exists():
        targets.append(OUTPUT_DIR / "final_paper.md")
    if MICRO_UNITS_DIR.exists():
        targets.extend(sorted(MICRO_UNITS_DIR.glob("*.txt")))

    bad_markers = ["内容生成中", "论文题目缺失", "关键词1；关键词2"]
    for path in targets:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for marker in bad_markers:
            if marker in text:
                warnings.append(f"{path}: 检测到占位痕迹 `{marker}`")
    return warnings


def run_pipeline() -> int:
    print("=== QA 流水线（quality-assurance-auditor）===")
    init_project()

    if not audit_gate("赛题目录检查"):
        return 1

    force_regenerate = os.environ.get("MATHMODEL_REGENERATE_TASKS") == "1"
    tasks, generated = generate_task_manifest(target_words=270, force=force_regenerate)
    action = "已生成" if generated else "已读取已有"
    print(f"[+] {action}任务清单：{TASKS_FILE}（{len(tasks)} 个微单元）")
    if PROBLEM_ANALYSIS_FILE.exists():
        print(f"[+] 已连接结构化赛题分析：{PROBLEM_ANALYSIS_FILE}")
    else:
        print("[!] 未找到 problem_analysis.json，已使用通用任务清单模板")

    ok, total, total_chars = verify_completeness()
    print(f"[+] 进度：{ok}/{total}")
    print(f"[+] 当前总长度：{total_chars}")

    warnings = scan_generated_text()
    if warnings:
        print("[!] 发现需要人工复核的占位痕迹：")
        for item in warnings[:20]:
            print(f"    - {item}")
        if len(warnings) > 20:
            print(f"    - ... 共 {len(warnings)} 项")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_pipeline())

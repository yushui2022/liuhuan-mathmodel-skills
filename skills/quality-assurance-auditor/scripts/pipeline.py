import json
import sys
from pathlib import Path


BASE_DIR = Path.cwd()
PROBLEM_DIR = BASE_DIR / "problem_files"
OUTPUT_DIR = BASE_DIR / "paper_output"
MICRO_UNITS_DIR = OUTPUT_DIR / "micro_units"
TASKS_FILE = OUTPUT_DIR / "tasks.json"


def init_project() -> None:
    for d in (PROBLEM_DIR, OUTPUT_DIR, MICRO_UNITS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def has_problem_files() -> bool:
    if not PROBLEM_DIR.exists():
        return False
    return any(PROBLEM_DIR.iterdir())


def generate_task_manifest(target_words: int = 300) -> list[dict]:
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
    return tasks


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


def run_pipeline() -> int:
    print("=== QA 流水线（quality-assurance-auditor）===")
    init_project()

    if not audit_gate("赛题目录检查"):
        return 1

    tasks = generate_task_manifest(target_words=270)
    print(f"[+] 已生成任务清单：{TASKS_FILE}（{len(tasks)} 个微单元）")

    ok, total, total_chars = verify_completeness()
    print(f"[+] 进度：{ok}/{total}")
    print(f"[+] 当前总长度：{total_chars}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_pipeline())

import os
import subprocess
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[4]
    os.chdir(root)

    print("=== Step-0 数据清洗与可视化 ===")
    r_clean = subprocess.run(
        ["python", ".trae/skills/data-cleaning-and-visualization/scripts/run_pipeline.py"],
        check=False,
    )
    if r_clean.returncode != 0:
        print("⚠️ 数据清洗步骤未成功执行（可能是没有数据文件），继续后续步骤...")

    print("=== Step-1 结果计算与出图 ===")
    r_calc = subprocess.run(
        ["python", "step2_calc_results.py"],
        check=False,
    )
    if r_calc.returncode != 0:
        return r_calc.returncode

    print("=== Step-2 质量审计与任务清单 ===")
    r0 = subprocess.run(
        ["python", ".trae/skills/quality-assurance-auditor/scripts/pipeline.py"],
        check=False,
    )
    if r0.returncode != 0:
        return r0.returncode

    print("=== Step-3 微单元离线生成 ===")
    r1 = subprocess.run(
        ["python", ".trae/skills/paper-micro-unit-generator/scripts/generate_all_offline.py"],
        check=False,
    )
    if r1.returncode != 0:
        return r1.returncode

    print("=== Step-4 合并 ===")
    r2 = subprocess.run(
        ["python", ".trae/skills/paper-micro-unit-generator/scripts/merge.py"],
        check=False,
    )
    if r2.returncode != 0:
        return r2.returncode

    print("✅ 已生成：paper_output/final_paper.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

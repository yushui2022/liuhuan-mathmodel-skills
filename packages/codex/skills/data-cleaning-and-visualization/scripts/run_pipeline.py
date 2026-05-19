import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root_dir = Path.cwd().resolve()
    os.chdir(root_dir)

    scripts_dir = Path("skills/data-cleaning-and-visualization/scripts")

    print("=== Step 0: 数据与图表计划 ===")
    plan_script = scripts_dir / "build_data_visualization_plan.py"
    if plan_script.exists():
        r0 = subprocess.run([sys.executable, str(plan_script)], check=False)
        if r0.returncode != 0:
            print("⚠️ 数据与图表计划未成功生成，继续执行清洗与可视化。")
    else:
        print("   未检测到数据与图表计划脚本，跳过。")

    print("\n=== Step 1: 数据清洗 (Data Cleaning) ===")
    clean_script = scripts_dir / "clean_data.py"
    r1 = subprocess.run([sys.executable, str(clean_script)], check=False)

    if r1.returncode != 0:
        print("❌ 数据清洗步骤失败，停止执行。")
        return r1.returncode

    print("\n=== Step 2: 数据可视化 (Data Visualization) ===")
    viz_script = scripts_dir / "visualize_data.py"
    r2 = subprocess.run([sys.executable, str(viz_script)], check=False)

    if r2.returncode != 0:
        print("❌ 数据可视化步骤失败。")
        return r2.returncode

    print("\n=== 数据清洗与可视化流程完成 ===")
    print("请查看 paper_output/ 目录获取结果。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

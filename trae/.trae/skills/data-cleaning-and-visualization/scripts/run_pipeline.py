import subprocess
import sys
import os
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parents[4]
    os.chdir(root_dir)
    
    scripts_dir = Path(".trae/skills/data-cleaning-and-visualization/scripts")
    
    print("🚀 === Step 1: 数据清洗 (Data Cleaning) ===")
    clean_script = scripts_dir / "clean_data.py"
    r1 = subprocess.run([sys.executable, str(clean_script)], check=False)
    
    if r1.returncode != 0:
        print("❌ 数据清洗步骤失败，停止执行。")
        return r1.returncode
        
    print("\n🚀 === Step 2: 数据可视化 (Data Visualization) ===")
    viz_script = scripts_dir / "visualize_data.py"
    r2 = subprocess.run([sys.executable, str(viz_script)], check=False)
    
    if r2.returncode != 0:
        print("❌ 数据可视化步骤失败。")
        return r2.returncode
        
    print("\n🎉 === 全流程执行完毕 (All Done) ===")
    print("请查看 paper_output/ 目录获取结果。")
    return 0

if __name__ == "__main__":
    sys.exit(main())

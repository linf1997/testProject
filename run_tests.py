"""
快速运行测试脚本
"""
import subprocess
import sys
import os

def main():
    """主函数"""
    print("=" * 50)
    print("接口自动化测试框架")
    print("=" * 50)
    
    # 检查是否安装了依赖
    try:
        import pytest
        import requests
        import openpyxl
        import yaml
        import allure
    except ImportError as e:
        print(f"错误: 缺少依赖包 {e.name}")
        print("请先运行: pip install -r requirements.txt")
        return
    
    # 运行pytest
    print("\n开始执行测试...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    print("\n" + "=" * 50)
    if result.returncode == 0:
        print("测试执行完成！")
        print("\n生成Allure报告请运行:")
        print("  allure generate reports/allure-results -o reports/allure-report --clean")
        print("  allure open reports/allure-report")
    else:
        print("测试执行失败，请查看日志文件")
    print("=" * 50)

if __name__ == "__main__":
    main()




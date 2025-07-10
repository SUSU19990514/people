#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel处理工作台演示脚本
展示完整的拆分和合并流程
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*50}")
    print(f"执行: {description}")
    print(f"命令: {cmd}")
    print('='*50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print("输出:")
            print(result.stdout)
        if result.stderr:
            print("错误:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"执行失败: {e}")
        return False

def main():
    """主演示函数"""
    print("Excel处理自动化工作台 - 完整演示")
    print("="*60)
    
    # 检查Python环境
    print("1. 检查Python环境...")
    if not run_command("python --version", "检查Python版本"):
        print("❌ Python环境检查失败")
        return
    
    # 安装依赖
    print("\n2. 安装依赖包...")
    if not run_command("pip install -r requirements.txt", "安装依赖"):
        print("❌ 依赖安装失败")
        return
    
    # 创建示例配置文件
    print("\n3. 创建配置文件...")
    if not run_command("python 花名册智能处理工具.py --create-config", "创建配置文件"):
        print("❌ 配置文件创建失败")
        return
    
    # 生成示例数据
    print("\n4. 生成示例数据...")
    if not run_command("python create_sample_data.py", "生成示例Excel文件"):
        print("❌ 示例数据生成失败")
        return
    
    # 检查文件是否存在
    if not Path("员工花名册.xlsx").exists():
        print("❌ 示例文件未生成")
        return
    
    # 执行拆分操作
    print("\n5. 执行拆分操作...")
    split_config = {
        "split_field": "部门",
        "keep_fields": ["员工编号", "姓名", "部门", "职位", "入职日期", "薪资"],
        "sort_fields": ["姓名"],
        "output_dir": "output",
        "sheet_name": "员工信息",
        "preserve_format": True
    }
    
    # 保存拆分配置
    import json
    with open('split_config.json', 'w', encoding='utf-8') as f:
        json.dump(split_config, f, ensure_ascii=False, indent=2)
    
    if not run_command("python 花名册智能处理工具.py --mode split --config split_config.json --input 员工花名册.xlsx", "按部门拆分"):
        print("❌ 拆分操作失败")
        return
    
    # 检查拆分结果
    output_dir = Path("output")
    if output_dir.exists():
        split_files = list(output_dir.glob("*.xlsx"))
        print(f"\n✅ 拆分完成，生成了 {len(split_files)} 个文件:")
        for file in split_files:
            print(f"  - {file.name}")
    
    # 执行合并操作
    print("\n6. 执行合并操作...")
    merge_config = {
        "keep_fields": ["员工编号", "姓名", "部门", "职位", "入职日期", "薪资"],
        "sort_fields": ["部门", "姓名"],
        "output_dir": "output",
        "sheet_name": "员工信息",
        "preserve_format": True
    }
    
    # 保存合并配置
    with open('merge_config.json', 'w', encoding='utf-8') as f:
        json.dump(merge_config, f, ensure_ascii=False, indent=2)
    
    # 获取拆分后的文件列表
    if output_dir.exists():
        split_files = list(output_dir.glob("*.xlsx"))
        if split_files:
            file_list = ",".join([str(f) for f in split_files])
            if not run_command(f'python 花名册智能处理工具.py --mode merge --config merge_config.json --input "{file_list}" --output 合并后花名册.xlsx', "合并拆分后的文件"):
                print("❌ 合并操作失败")
                return
    
    # 最终结果展示
    print("\n7. 最终结果...")
    print("✅ 演示完成！")
    print("\n生成的文件:")
    
    files_to_check = [
        "员工花名册.xlsx",
        "合并后花名册.xlsx",
        "config.json",
        "config.yaml",
        "split_config.json",
        "merge_config.json"
    ]
    
    for file in files_to_check:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (未生成)")
    
    if output_dir.exists():
        print(f"  📁 output/ (包含拆分后的文件)")
    
    print("\n使用说明:")
    print("1. 修改配置文件中的参数来适应您的需求")
    print("2. 使用 --mode split 进行拆分操作")
    print("3. 使用 --mode merge 进行合并操作")
    print("4. 查看 excel_processor.log 获取详细日志")

if __name__ == "__main__":
    main() 
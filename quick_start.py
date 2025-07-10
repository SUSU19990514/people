#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel处理工作台 - 快速启动脚本
提供交互式界面，方便用户快速使用
"""

import os
import sys
import json
from pathlib import Path
from 花名册智能处理工具 import ExcelProcessor, ProcessingConfig, create_sample_config

def print_banner():
    """打印欢迎横幅"""
    print("="*60)
    print("    Excel处理自动化工作台 - 快速启动")
    print("="*60)
    print("功能: 智能拆分 | 智能合并 | 格式保留 | 配置化处理")
    print("="*60)

def get_user_choice():
    """获取用户选择"""
    print("\n请选择操作:")
    print("1. 创建示例配置文件")
    print("2. 生成示例数据")
    print("3. 拆分Excel文件")
    print("4. 合并Excel文件")
    print("5. 运行完整演示")
    print("0. 退出")
    
    while True:
        choice = input("\n请输入选项 (0-5): ").strip()
        if choice in ['0', '1', '2', '3', '4', '5']:
            return choice
        print("❌ 无效选项，请重新输入")

def create_config_interactive():
    """交互式创建配置"""
    print("\n📝 创建配置文件")
    print("-" * 30)
    
    config = {}
    
    # 拆分字段
    split_field = input("请输入拆分字段名 (如: 部门): ").strip()
    if split_field:
        config['split_field'] = split_field
    
    # 保留字段
    keep_fields_input = input("请输入保留字段 (用逗号分隔，如: 姓名,部门,职位): ").strip()
    if keep_fields_input:
        config['keep_fields'] = [f.strip() for f in keep_fields_input.split(',')]
    
    # 排序字段
    sort_fields_input = input("请输入排序字段 (用逗号分隔，如: 部门,姓名): ").strip()
    if sort_fields_input:
        config['sort_fields'] = [f.strip() for f in sort_fields_input.split(',')]
    
    # 输出目录
    output_dir = input("请输入输出目录 (默认: output): ").strip()
    config['output_dir'] = output_dir if output_dir else 'output'
    
    # 工作表名称
    sheet_name = input("请输入工作表名称 (默认: Sheet1): ").strip()
    config['sheet_name'] = sheet_name if sheet_name else 'Sheet1'
    
    # 是否保留格式
    preserve_format = input("是否保留格式? (y/n, 默认: y): ").strip().lower()
    config['preserve_format'] = preserve_format != 'n'
    
    # 保存配置
    config_file = input("请输入配置文件名 (默认: my_config.json): ").strip()
    if not config_file:
        config_file = 'my_config.json'
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置文件已保存: {config_file}")
    return config_file

def split_excel_interactive():
    """交互式拆分Excel"""
    print("\n📊 拆分Excel文件")
    print("-" * 30)
    
    # 获取配置文件
    config_file = input("请输入配置文件路径 (或按回车创建新配置): ").strip()
    if not config_file:
        config_file = create_config_interactive()
    
    # 获取输入文件
    input_file = input("请输入要拆分的Excel文件路径: ").strip()
    if not Path(input_file).exists():
        print(f"❌ 文件不存在: {input_file}")
        return
    
    try:
        # 加载配置
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        config = ProcessingConfig(**config_data)
        processor = ExcelProcessor(config)
        
        # 执行拆分
        processor.split_excel(input_file)
        print("✅ 拆分完成！")
        
    except Exception as e:
        print(f"❌ 拆分失败: {e}")

def merge_excel_interactive():
    """交互式合并Excel"""
    print("\n🔗 合并Excel文件")
    print("-" * 30)
    
    # 获取配置文件
    config_file = input("请输入配置文件路径 (或按回车创建新配置): ").strip()
    if not config_file:
        config_file = create_config_interactive()
    
    # 获取输入文件列表
    input_files_input = input("请输入要合并的Excel文件路径 (用逗号分隔): ").strip()
    input_files = [f.strip() for f in input_files_input.split(',')]
    
    # 检查文件是否存在
    for file_path in input_files:
        if not Path(file_path).exists():
            print(f"❌ 文件不存在: {file_path}")
            return
    
    # 获取输出文件
    output_file = input("请输入合并后的输出文件路径: ").strip()
    
    try:
        # 加载配置
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        config = ProcessingConfig(**config_data)
        processor = ExcelProcessor(config)
        
        # 执行合并
        processor.merge_excel_files(input_files, output_file)
        print("✅ 合并完成！")
        
    except Exception as e:
        print(f"❌ 合并失败: {e}")

def generate_sample_data():
    """生成示例数据"""
    print("\n📋 生成示例数据")
    print("-" * 30)
    
    try:
        # 导入并执行示例数据生成
        from create_sample_data import create_sample_excel
        create_sample_excel()
        print("✅ 示例数据生成完成！")
        
    except ImportError:
        print("❌ 找不到 create_sample_data.py 文件")
    except Exception as e:
        print(f"❌ 生成示例数据失败: {e}")

def run_full_demo():
    """运行完整演示"""
    print("\n🎬 运行完整演示")
    print("-" * 30)
    
    try:
        # 导入并执行演示脚本
        from demo import main as demo_main
        demo_main()
        
    except ImportError:
        print("❌ 找不到 demo.py 文件")
    except Exception as e:
        print(f"❌ 运行演示失败: {e}")

def main():
    """主函数"""
    print_banner()
    
    while True:
        choice = get_user_choice()
        
        if choice == '0':
            print("\n👋 感谢使用Excel处理工作台！")
            break
        elif choice == '1':
            create_sample_config()
            print("✅ 示例配置文件已创建")
        elif choice == '2':
            generate_sample_data()
        elif choice == '3':
            split_excel_interactive()
        elif choice == '4':
            merge_excel_interactive()
        elif choice == '5':
            run_full_demo()
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main() 
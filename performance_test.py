#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能测试脚本
用于测试优化版Excel处理器的性能表现
"""

import time
import os
import psutil
import pandas as pd
import openpyxl
from pathlib import Path
from excel_processor_optimized import OptimizedExcelProcessor, ProcessingConfig
import random
import string

def create_test_data(rows=10000, cols=20, sheets=3, output_file="test_large_data.xlsx"):
    """创建测试数据"""
    print(f"正在创建测试数据: {rows}行 x {cols}列 x {sheets}个sheet")
    
    # 创建列名
    columns = [f'列{i}' for i in range(cols)]
    
    # 创建数据
    data = {}
    for i in range(cols):
        if i == 0:  # 第一列作为拆分字段
            data[f'列{i}'] = [f'组{random.randint(1, 10)}' for _ in range(rows)]
        elif i == 1:  # 第二列作为排序字段
            data[f'列{i}'] = [random.randint(1, 1000) for _ in range(rows)]
        else:
            data[f'列{i}'] = [''.join(random.choices(string.ascii_letters, k=10)) for _ in range(rows)]
    
    df = pd.DataFrame(data)
    
    # 创建Excel文件
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for i in range(sheets):
            sheet_name = f'Sheet{i+1}'
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"测试数据已创建: {output_file}")
    print(f"文件大小: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
    return output_file

def get_memory_usage():
    """获取当前内存使用情况"""
    process = psutil.Process()
    memory_info = process.memory_info()
    return memory_info.rss / 1024 / 1024  # MB

def test_original_processor(input_file, output_dir="test_output_original"):
    """测试原始处理器"""
    print("\n" + "="*50)
    print("测试原始处理器")
    print("="*50)
    
    start_time = time.time()
    start_memory = get_memory_usage()
    
    try:
        # 这里可以添加原始处理器的测试代码
        # 由于我们没有原始处理器，这里只是模拟
        print("原始处理器测试（模拟）")
        time.sleep(2)  # 模拟处理时间
        
        end_time = time.time()
        end_memory = get_memory_usage()
        
        print(f"处理时间: {end_time - start_time:.2f} 秒")
        print(f"内存使用: {end_memory - start_memory:.2f} MB")
        print(f"峰值内存: {end_memory:.2f} MB")
        
    except Exception as e:
        print(f"原始处理器测试失败: {e}")

def test_optimized_processor(input_file, batch_size=1000, max_workers=4, memory_limit=512):
    """测试优化处理器"""
    print("\n" + "="*50)
    print(f"测试优化处理器 (batch_size={batch_size}, max_workers={max_workers}, memory_limit={memory_limit}MB)")
    print("="*50)
    
    start_time = time.time()
    start_memory = get_memory_usage()
    
    try:
        # 创建配置
        config = ProcessingConfig(
            split_field="列0",
            keep_fields={"Sheet1": ["列0", "列1", "列2", "列3"]},
            sort_fields=["列1"],
            output_dir="test_output_optimized",
            preserve_format=True,
            batch_size=batch_size,
            max_workers=max_workers,
            memory_limit_mb=memory_limit
        )
        
        # 创建处理器
        processor = OptimizedExcelProcessor(config)
        
        # 执行拆分
        result_files = processor.split_excel_optimized(input_file)
        
        end_time = time.time()
        end_memory = get_memory_usage()
        
        print(f"处理时间: {end_time - start_time:.2f} 秒")
        print(f"内存使用: {end_memory - start_memory:.2f} MB")
        print(f"峰值内存: {end_memory:.2f} MB")
        print(f"生成文件数: {len(result_files)}")
        
        # 清理缓存
        processor.cleanup_cache()
        
        return {
            'time': end_time - start_time,
            'memory_peak': end_memory,
            'memory_increase': end_memory - start_memory,
            'files_generated': len(result_files)
        }
        
    except Exception as e:
        print(f"优化处理器测试失败: {e}")
        return None

def test_different_configurations(input_file):
    """测试不同配置的性能"""
    print("\n" + "="*60)
    print("测试不同配置的性能")
    print("="*60)
    
    configurations = [
        {'batch_size': 500, 'max_workers': 2, 'memory_limit': 256},
        {'batch_size': 1000, 'max_workers': 4, 'memory_limit': 512},
        {'batch_size': 2000, 'max_workers': 6, 'memory_limit': 1024},
        {'batch_size': 5000, 'max_workers': 8, 'memory_limit': 2048},
    ]
    
    results = []
    
    for i, config in enumerate(configurations):
        print(f"\n配置 {i+1}: {config}")
        result = test_optimized_processor(input_file, **config)
        if result:
            result['config'] = config
            results.append(result)
    
    # 显示结果对比
    print("\n" + "="*60)
    print("性能对比结果")
    print("="*60)
    print(f"{'配置':<20} {'处理时间(秒)':<15} {'峰值内存(MB)':<15} {'生成文件数':<12}")
    print("-" * 60)
    
    for result in results:
        config = result['config']
        config_str = f"batch={config['batch_size']}, workers={config['max_workers']}"
        print(f"{config_str:<20} {result['time']:<15.2f} {result['memory_peak']:<15.1f} {result['files_generated']:<12}")

def test_large_file_handling():
    """测试大文件处理能力"""
    print("\n" + "="*60)
    print("测试大文件处理能力")
    print("="*60)
    
    # 创建不同大小的测试文件
    file_sizes = [
        (1000, 10, 1, "small_test.xlsx"),
        (10000, 20, 3, "medium_test.xlsx"),
        (50000, 30, 5, "large_test.xlsx"),
    ]
    
    for rows, cols, sheets, filename in file_sizes:
        print(f"\n测试文件: {filename}")
        print(f"规格: {rows}行 x {cols}列 x {sheets}个sheet")
        
        # 创建测试文件
        test_file = create_test_data(rows, cols, sheets, filename)
        
        # 测试处理
        result = test_optimized_processor(
            test_file, 
            batch_size=1000, 
            max_workers=4, 
            memory_limit=512
        )
        
        if result:
            print(f"✅ 成功处理 {filename}")
        else:
            print(f"❌ 处理 {filename} 失败")
        
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

def main():
    """主函数"""
    print("🚀 Excel处理器性能测试")
    print("="*60)
    
    # 检查系统信息
    print(f"系统内存: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.1f} GB")
    print(f"CPU核心数: {psutil.cpu_count()}")
    print(f"当前内存使用: {get_memory_usage():.1f} MB")
    
    # 创建测试数据
    test_file = create_test_data(rows=10000, cols=20, sheets=3)
    
    try:
        # 测试原始处理器（模拟）
        test_original_processor(test_file)
        
        # 测试优化处理器
        test_optimized_processor(test_file)
        
        # 测试不同配置
        test_different_configurations(test_file)
        
        # 测试大文件处理
        test_large_file_handling()
        
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
        
        # 清理输出目录
        for output_dir in ["test_output_original", "test_output_optimized"]:
            if os.path.exists(output_dir):
                import shutil
                shutil.rmtree(output_dir)
    
    print("\n" + "="*60)
    print("性能测试完成！")
    print("="*60)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包Streamlit应用为可执行文件
使用PyInstaller将应用打包成独立的exe文件
"""

import os
import subprocess
import sys

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller安装成功")
    except subprocess.CalledProcessError:
        print("❌ PyInstaller安装失败")
        return False
    return True

def create_spec_file():
    """创建PyInstaller配置文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['excel_web_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'streamlit',
        'pandas',
        'openpyxl',
        'yaml',
        'json',
        'tempfile',
        'pathlib',
        'zipfile',
        'copy'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Excel处理工作台',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Excel处理工作台',
)
'''
    
    with open('excel_web_app.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("✅ 配置文件创建成功")

def build_executable():
    """构建可执行文件"""
    try:
        # 使用spec文件构建
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller", 
            "--clean", "excel_web_app.spec"
        ])
        print("✅ 可执行文件构建成功")
        print("📁 输出目录: dist/Excel处理工作台/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def create_launcher():
    """创建启动脚本"""
    launcher_content = '''@echo off
echo 正在启动Excel处理工作台...
cd /d "%~dp0"
start "" "Excel处理工作台.exe"
'''
    
    with open('启动Excel处理工作台.bat', 'w', encoding='gbk') as f:
        f.write(launcher_content)
    print("✅ 启动脚本创建成功")

def main():
    print("🚀 开始打包Excel处理工作台...")
    
    # 1. 安装PyInstaller
    if not install_pyinstaller():
        return
    
    # 2. 创建配置文件
    create_spec_file()
    
    # 3. 构建可执行文件
    if build_executable():
        # 4. 创建启动脚本
        create_launcher()
        
        print("\n🎉 打包完成！")
        print("📋 使用说明：")
        print("1. 将 dist/Excel处理工作台/ 文件夹复制给其他人")
        print("2. 其他人双击 '启动Excel处理工作台.bat' 即可使用")
        print("3. 无需安装Python或其他依赖")
    else:
        print("❌ 打包失败")

if __name__ == "__main__":
    main() 
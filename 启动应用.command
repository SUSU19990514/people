#!/bin/bash

echo "🚀 启动Excel处理工作台..."
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查可执行文件
if [ -f "Excel处理工作台" ]; then
    echo "✅ 找到可执行文件"
    echo "🌐 正在启动，浏览器将自动打开 http://localhost:8501"
    echo ""
    echo "💡 提示：关闭此窗口即可停止应用"
    echo ""
    
    # 启动应用
    ./"Excel处理工作台"
    
elif [ -f "dist/Excel处理工作台/Excel处理工作台" ]; then
    echo "✅ 找到可执行文件（在dist目录中）"
    echo "🌐 正在启动，浏览器将自动打开 http://localhost:8501"
    echo ""
    echo "💡 提示：关闭此窗口即可停止应用"
    echo ""
    
    # 启动应用
    cd "dist/Excel处理工作台"
    ./"Excel处理工作台"
    
else
    echo "❌ 错误：找不到可执行文件"
    echo "请确保此脚本与可执行文件在同一目录下"
    echo ""
    read -p "按任意键退出..."
fi 
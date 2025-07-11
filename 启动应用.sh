#!/bin/bash

# Excel处理自动化工作台启动脚本

echo "🚀 启动Excel处理自动化工作台..."

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 虚拟环境不存在，正在创建..."
    python3 -m venv .venv
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source .venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements_optimized.txt

# 启动应用
echo "🌐 启动Streamlit应用..."
echo "📍 应用将在浏览器中打开: http://localhost:8501"
echo "🔄 按 Ctrl+C 停止应用"
echo ""

streamlit run excel_web_app_optimized.py 
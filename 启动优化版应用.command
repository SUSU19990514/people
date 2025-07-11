#!/bin/bash

# Excel处理工作台 - 优化版启动脚本
# 专为大规模数据处理优化

echo "🚀 启动Excel处理工作台 - 优化版"
echo "=================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到Python3，请先安装Python"
    exit 1
fi

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source .venv/bin/activate

# 安装依赖
echo "📥 安装优化版依赖..."
pip install -r requirements_optimized.txt

# 检查依赖安装
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败，请检查网络连接或手动安装"
    exit 1
fi

# 创建输出目录
mkdir -p output

# 显示系统信息
echo ""
echo "💻 系统信息："
echo "Python版本: $(python3 --version)"
echo "系统内存: $(sysctl -n hw.memsize | awk '{print $0/1024/1024/1024 " GB"}')"
echo "CPU核心数: $(sysctl -n hw.ncpu)"
echo ""

# 启动应用
echo "🌐 启动优化版Web应用..."
echo "访问地址: http://localhost:8501"
echo "按 Ctrl+C 停止应用"
echo ""

streamlit run excel_web_app_optimized.py --server.port 8501 --server.address localhost 
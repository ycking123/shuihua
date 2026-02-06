#!/bin/bash

# 脚本说明：自动修复依赖安装时的编译错误
# 作用：安装 gcc/g++ 编译器，升级 pip，并优先使用 Conda 安装二进制包

echo "========================================="
echo "   Fixing Dependency Installation Issues"
echo "========================================="

# 1. 升级 pip (关键：新版 pip 能找到更多预编译的 wheel 包，避免源码编译)
echo "[1/4] Upgrading pip..."
pip install --upgrade pip setuptools wheel

# 2. 安装系统级编译器 (解决 'command 'g++' failed' 错误)
echo "[2/4] Checking for system compilers..."
if command -v yum &> /dev/null; then
    echo "Detected YUM (CentOS/Alibaba Linux). Installing gcc-c++..."
    yum install -y gcc gcc-c++ python3-devel
elif command -v apt-get &> /dev/null; then
    echo "Detected APT (Ubuntu/Debian). Installing build-essential..."
    apt-get update
    apt-get install -y build-essential python3-dev
else
    echo "Warning: Could not detect package manager (yum/apt). Skipping system compiler install."
fi

# 3. 优先使用 Conda 安装难编译的包 (解决 greenlet, sqlalchemy, tiktoken 等问题)
# Conda 仓库中的包是预编译好的，不需要本地 gcc/rust 环境
# 另外，安装 gxx_linux-64 可以提供现代化的编译器，解决 pip 源码编译时的"编译器过旧"问题
echo "[3/4] Installing binary packages and compilers via Conda..."
if command -v conda &> /dev/null; then
    # 安装 sqlalchemy 等二进制包
    # 安装 gxx_linux-64 (现代 C++ 编译器) 以支持 pip 编译其他包
    conda install -y -c conda-forge sqlalchemy pymysql cryptography tiktoken gxx_linux-64 gcc_linux-64 sysroot_linux-64
else
    echo "Warning: 'conda' command not found. Trying to source conda profile..."
    # 尝试加载 conda 环境 (假设安装在常见位置)
    for conda_path in "$HOME/miniconda3" "$HOME/anaconda3" "/opt/miniconda3" "/usr/local/miniconda3" "/home/shuihua-agent/miniconda3"; do
        if [ -f "$conda_path/etc/profile.d/conda.sh" ]; then
            source "$conda_path/etc/profile.d/conda.sh"
            echo "Loaded conda from $conda_path"
            conda install -y -c conda-forge sqlalchemy pymysql cryptography tiktoken gxx_linux-64 gcc_linux-64 sysroot_linux-64
            break
        fi
    done
fi

# 3.5 再次强制检查并安装关键依赖 (针对 sqlalchemy 缺失的情况)
echo "[3.5/4] Verifying and forcing install of critical dependencies..."
if ! python -c "import sqlalchemy" &> /dev/null; then
    echo "sqlalchemy missing. Attempting pip install with binary preference..."
    pip install --upgrade --force-reinstall --prefer-binary sqlalchemy pymysql
fi

# 4. 再次尝试安装 requirements.txt
echo "[4/4] Installing remaining python dependencies..."
pip install -r requirements.txt

echo "========================================="
echo "   Repair Complete! Please restart server."
echo "========================================="


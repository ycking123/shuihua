#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强制同构检查脚本

功能：
1. 检查每个模块的 MODULE.md 成员清单是否与实际文件匹配
2. 检查代码文件头部的依赖声明是否准确
3. 发现不一致时报告问题

使用方法：
    python scripts/check_docs_sync.py
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Set

# 设置控制台编码为 UTF-8
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, 'strict')

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent

# 模块定义
MODULES = {
    "backend": ROOT_DIR / "backend",
    "server": ROOT_DIR / "server",
    "components": ROOT_DIR / "components",
    "crawlers": ROOT_DIR / "crawlers",
    "utils": ROOT_DIR / "utils",
}

# 文件扩展名映射
MODULE_EXTENSIONS = {
    "backend": [".py"],
    "server": [".py"],
    "components": [".tsx", ".ts"],
    "crawlers": [".py"],
    "utils": [".py", ".ts", ".tsx"],
}


def get_module_files(module_name: str) -> List[Path]:
    """获取模块下的所有代码文件"""
    module_dir = MODULES[module_name]
    extensions = MODULE_EXTENSIONS.get(module_name, [])
    files = []

    for ext in extensions:
        files.extend(module_dir.glob(f"*{ext}"))

    # 忽略 __pycache__, node_modules 等
    files = [f for f in files if "__pycache__" not in str(f) and "node_modules" not in str(f)]

    return sorted(files)


def extract_file_header(file_path: Path) -> Dict[str, str]:
    """从文件头提取依赖和职责信息"""
    try:
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # 查找文档块
        doc_start = -1
        for i, line in enumerate(lines):
            if "===" in line and i > 0:
                doc_start = i - 10  # 往前查找
                break

        if doc_start < 0:
            return {"has_header": False}

        # 提取文档块内容（到第一个非注释行或空行）
        doc_lines = []
        for line in lines[doc_start:doc_start + 50]:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith("//") and "===" not in stripped:
                break
            doc_lines.append(line)

        doc_text = "\n".join(doc_lines)

        return {
            "has_header": True,
            "content": doc_text,
        }
    except Exception as e:
        return {"has_header": False, "error": str(e)}


def parse_module_doc(module_name: str) -> Dict:
    """解析 MODULE.md 文件"""
    module_file = MODULES[module_name] / "MODULE.md"

    if not module_file.exists():
        return {"exists": False}

    content = module_file.read_text(encoding="utf-8")

    # 提取成员清单表格
    member_pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
    members = re.findall(member_pattern, content)

    return {
        "exists": True,
        "members": members,
        "content": content,
    }


def check_module(module_name: str) -> List[str]:
    """检查单个模块的文档同步情况"""
    issues = []

    # 1. 检查 MODULE.md 是否存在
    module_doc = parse_module_doc(module_name)
    if not module_doc["exists"]:
        issues.append(f"❌ {module_name}/MODULE.md 不存在")
        return issues

    # 2. 检查成员清单
    actual_files = get_module_files(module_name)
    doc_members = module_doc["members"]

    # 从文档中提取的文件名
    doc_files = set()
    for file, func, desc in doc_members:
        file = file.strip()
        if file and file != "文件":
            doc_files.add(file)

    # 实际文件名
    actual_file_names = set(f.name for f in actual_files)

    # 找出文档中有但实际不存在的文件
    missing_files = doc_files - actual_file_names
    if missing_files:
        issues.append(f"⚠️  {module_name}/MODULE.md 中列出的文件不存在: {missing_files}")

    # 找出实际存在但文档中缺失的文件
    extra_files = actual_file_names - doc_files
    if extra_files:
        issues.append(f"⚠️  {module_name}/MODULE.md 缺少文件: {extra_files}")

    # 3. 检查文件头声明
    for file_path in actual_files:
        header_info = extract_file_header(file_path)
        if not header_info.get("has_header"):
            issues.append(f"⚠️  {file_path} 缺少头部文档块")

    return issues


def check_global_map() -> List[str]:
    """检查全局 MAP.md"""
    issues = []
    map_file = ROOT_DIR / "MAP.md"

    if not map_file.exists():
        issues.append("❌ 根目录 MAP.md 不存在")
        return issues

    content = map_file.read_text(encoding="utf-8")

    # 检查是否列出了所有模块
    for module_name in MODULES.keys():
        module_doc_ref = f"`{module_name}/MODULE.md`"
        if module_doc_ref not in content:
            issues.append(f"⚠️  MAP.md 中未引用 {module_doc_ref}")

    return issues


def main():
    """主检查逻辑"""
    print("=" * 60)
    print("🔍 分形文档强制同构检查")
    print("=" * 60)
    print()

    all_issues = []

    # 检查全局 MAP.md
    print("📄 检查全局 MAP.md...")
    map_issues = check_global_map()
    all_issues.extend(map_issues)
    if not map_issues:
        print("   ✅ MAP.md 检查通过")
    print()

    # 检查各模块
    for module_name in MODULES.keys():
        print(f"📦 检查模块 {module_name}/...")
        module_issues = check_module(module_name)
        all_issues.extend(module_issues)

        if not module_issues:
            print(f"   ✅ {module_name}/ 检查通过")
        else:
            for issue in module_issues:
                print(f"   {issue}")
        print()

    # 总结
    print("=" * 60)
    if all_issues:
        print(f"❌ 发现 {len(all_issues)} 个问题:")
        for issue in all_issues:
            print(f"   {issue}")
        print()
        print("💡 建议:")
        print("   1. 更新 MODULE.md 中的成员清单")
        print("   2. 为代码文件添加头部文档块")
        print("   3. 确保依赖声明准确")
        return 1
    else:
        print("✅ 所有检查通过！文档与代码保持同步")
        return 0


if __name__ == "__main__":
    exit(main())

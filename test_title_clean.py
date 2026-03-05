#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试会议标题清理功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def _clean_title_prefix(title: str) -> str:
    """清理标题中的无效前缀和后缀"""
    prefix_patterns = [
        "这是一场关于",
        "这是一场",
        "本次会议是关于",
        "本次会议",
        "会议内容：",
        "【AI 智能总览】",
        "【章节内容详情】",
        "【发言人观点整合】",
    ]
    
    for prefix in prefix_patterns:
        if title.startswith(prefix):
            title = title[len(prefix):].strip()
            break
    
    suffix_patterns = ["的讨论会", "的会议", "讨论会", "会议"]
    for suffix in suffix_patterns:
        if title.endswith(suffix) and len(title) > len(suffix) + 2:
            title = title[:-len(suffix)]
            break
    
    return title.strip()

def test_title_clean():
    """测试标题清理功能"""
    print("=" * 70)
    print("📋 会议标题清理功能测试")
    print("=" * 70)
    
    test_cases = [
        ("这是一场关于企业微信API集成与智能助手功能开发的讨论会", "企业微信API集成与智能助手功能开发"),
        ("这是一场关于技术分享的会议", "技术分享"),
        ("这是一场技术分享会议", "技术分享"),
        ("本次会议是关于项目进度汇报", "项目进度汇报"),
        ("本次会议讨论了新产品发布计划", "讨论了新产品发布计划"),
        ("会议内容：讨论Q4销售目标", "讨论Q4销售目标"),
        ("【AI 智能总览】讨论了系统架构优化问题", "讨论了系统架构优化问题"),
        ("【章节内容详情】1. 项目背景介绍", "1. 项目背景介绍"),
        ("正常的会议标题", "正常的会议标题"),
        ("产品需求评审会", "产品需求评审会"),
    ]
    
    passed = 0
    failed = 0
    
    for input_title, expected in test_cases:
        result = _clean_title_prefix(input_title)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        else:
            failed += 1
        print(f"{status} 输入: {input_title[:40]}...")
        print(f"   期望: {expected}")
        print(f"   结果: {result}")
        print()
    
    print("=" * 70)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    print("=" * 70)
    
    return failed == 0

if __name__ == "__main__":
    success = test_title_clean()
    sys.exit(0 if success else 1)

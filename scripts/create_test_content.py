#!/usr/bin/env python3
"""
测试多语言内容生成
"""

import json
from pathlib import Path
from datetime import datetime

def create_test_content():
    """创建测试内容"""
    
    # 中文测试内容
    zh_content = """---
title: "人工智能技术突破新算法提升机器学习效率50%"
date: 2025-07-11T12:00:00+08:00
categories: ["tech"]
tags: ["人工智能", "机器学习", "算法"]
summary: "最新研究表明，新的深度学习算法可以显著提升机器学习模型的训练效率"
source_url: "https://example.com/ai-breakthrough"
---

最新研究表明，新的深度学习算法可以显著提升机器学习模型的训练效率，相比传统方法提升了50%的性能。这一突破将对人工智能领域产生深远影响。

---

*来源: [原文链接](https://example.com/ai-breakthrough)*
"""
    
    # 英文测试内容
    en_content = """---
title: "AI Technology Breakthrough: New Algorithm Boosts Machine Learning Efficiency by 50%"
date: 2025-07-11T12:00:00+08:00
categories: ["tech"]
tags: ["artificial intelligence", "machine learning", "algorithm"]
summary: "Latest research shows new deep learning algorithms can significantly improve ML model training efficiency"
source_url: "https://example.com/ai-breakthrough"
---

Latest research shows that new deep learning algorithms can significantly improve machine learning model training efficiency, with a 50% performance boost compared to traditional methods. This breakthrough will have far-reaching implications for the AI field.

---

*Source: [Original Link](https://example.com/ai-breakthrough)*
"""
    
    # 创建目录和文件
    zh_dir = Path('../content/zh/tech')
    en_dir = Path('../content/en/tech')
    
    zh_dir.mkdir(parents=True, exist_ok=True)
    en_dir.mkdir(parents=True, exist_ok=True)
    
    # 写入测试文件
    with open(zh_dir / '2025-07-11-ai-breakthrough-zh.md', 'w', encoding='utf-8') as f:
        f.write(zh_content)
    
    with open(en_dir / '2025-07-11-ai-breakthrough-en.md', 'w', encoding='utf-8') as f:
        f.write(en_content)
    
    print("Test content created successfully!")
    print("Created files:")
    print("- content/zh/tech/2025-07-11-ai-breakthrough-zh.md")
    print("- content/en/tech/2025-07-11-ai-breakthrough-en.md")

if __name__ == "__main__":
    create_test_content()
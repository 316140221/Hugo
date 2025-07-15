#!/usr/bin/env python3
"""
生成多语言测试内容
"""

import os
from pathlib import Path
from datetime import datetime, timedelta

def create_sample_content():
    """创建示例内容"""
    
    # 中文内容示例
    zh_articles = [
        {
            "category": "tech",
            "title": "苹果发布最新iPhone 16系列搭载A18芯片性能提升30%",
            "summary": "苹果公司今日正式发布iPhone 16系列，搭载全新A18芯片，性能相比上代提升30%",
            "content": "苹果公司在今日的发布会上正式推出了iPhone 16系列手机，新机搭载了自主研发的A18芯片，采用3纳米工艺制程，性能相比A17芯片提升了30%。新iPhone还配备了更先进的摄像系统和更长的电池续航时间。"
        },
        {
            "category": "finance", 
            "title": "央行下调存款准备金率0.5个百分点释放流动性约1万亿",
            "summary": "中国人民银行宣布下调金融机构存款准备金率0.5个百分点，此举将释放长期资金约1万亿元",
            "content": "中国人民银行今日宣布，为保持银行体系流动性合理充裕，促进货币信贷平稳增长，决定于近期下调金融机构存款准备金率0.5个百分点。此次降准将释放长期资金约1万亿元，有助于维护货币市场利率平稳运行。"
        },
        {
            "category": "entertainment",
            "title": "漫威新片《银河护卫队3》全球票房突破10亿美元",
            "summary": "漫威影业出品的《银河护卫队3》上映三周后全球累计票房突破10亿美元大关",
            "content": "漫威影业出品的超级英雄电影《银河护卫队3》自上映以来表现强劲，截至目前全球累计票房已突破10亿美元大关。该片作为银河护卫队三部曲的收官之作，获得了影迷和评论家的一致好评。"
        }
    ]
    
    # 英文内容示例
    en_articles = [
        {
            "category": "tech",
            "title": "Apple Unveils iPhone 16 Series with A18 Chip, 30% Performance Boost",
            "summary": "Apple officially launched the iPhone 16 series today, featuring the new A18 chip with 30% better performance",
            "content": "Apple officially unveiled the iPhone 16 series at today's event, featuring the company's new A18 chip built on 3nm process technology, delivering 30% better performance than the A17 chip. The new iPhones also feature an advanced camera system and longer battery life."
        },
        {
            "category": "finance",
            "title": "Federal Reserve Cuts Interest Rates by 0.25 Percentage Points",
            "summary": "The Federal Reserve announced a 0.25 percentage point cut to the federal funds rate amid economic uncertainty",
            "content": "The Federal Reserve announced today a 0.25 percentage point reduction in the federal funds rate, bringing it to a new range. The decision comes as policymakers aim to support economic growth while maintaining price stability in an uncertain global environment."
        },
        {
            "category": "entertainment", 
            "title": "Marvel's Guardians of the Galaxy Vol. 3 Crosses $1 Billion Worldwide",
            "summary": "Marvel Studios' Guardians of the Galaxy Vol. 3 has crossed the $1 billion mark at the global box office",
            "content": "Marvel Studios' Guardians of the Galaxy Vol. 3 has achieved a major milestone, crossing $1 billion at the worldwide box office three weeks after its release. The film, which serves as the conclusion to the Guardians trilogy, has received critical acclaim and strong audience response."
        }
    ]
    
    base_date = datetime.now() - timedelta(days=2)
    
    # 创建中文内容
    for i, article in enumerate(zh_articles):
        article_date = base_date + timedelta(hours=i*6)
        create_article_file(article, 'zh', article_date)
    
    # 创建英文内容 
    for i, article in enumerate(en_articles):
        article_date = base_date + timedelta(hours=i*6)
        create_article_file(article, 'en', article_date)

def create_article_file(article, language, date):
    """创建文章文件"""
    
    content_dir = Path(f'../content/{language}/{article["category"]}')
    content_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    safe_title = article["title"][:50].replace(' ', '-').replace('/', '-').replace(':', '-')
    filename = f'{date.strftime("%Y-%m-%d")}-{safe_title}.md'
    
    # 创建文章内容
    article_content = f'''---
title: "{article["title"]}"
date: {date.strftime('%Y-%m-%dT%H:%M:%S+08:00')}
categories: ["{article["category"]}"]
tags: []
summary: "{article["summary"]}"
source_url: "https://example.com/news"
---

{article["content"]}

---

*来源: [原文链接](https://example.com/news)*
'''
    
    filepath = content_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article_content)
    
    print(f"Created: {filepath}")

if __name__ == "__main__":
    create_sample_content()
    print("Sample content created successfully!")
#!/usr/bin/env python3
"""
多语言内容聚合脚本 - 自动抓取中英文新闻资讯
"""

import requests
import feedparser
import json
import os
from datetime import datetime
import re
from pathlib import Path

class MultilingualContentAggregator:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.content_dir = Path('../content')
        
    def load_config(self, config_file):
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_default_config()
    
    def get_default_config(self):
        """默认配置"""
        return {
            "rss_feeds": {
                "zh": {
                    "tech": ["https://feeds.feedburner.com/TechCrunch"],
                    "finance": ["https://feeds.finance.yahoo.com/rss/2.0/headline"],
                    "entertainment": ["https://www.hollywoodreporter.com/feed/"]
                },
                "en": {
                    "tech": ["https://feeds.feedburner.com/TechCrunch"],
                    "finance": ["https://feeds.finance.yahoo.com/rss/2.0/headline"],
                    "entertainment": ["https://www.hollywoodreporter.com/feed/"]
                }
            },
            "max_articles_per_feed": 5,
            "content_length_limit": 1000
        }
    
    def clean_content(self, content):
        """清理内容"""
        # 移除HTML标签
        content = re.sub(r'<[^>]+>', '', content)
        # 移除多余的空白
        content = re.sub(r'\s+', ' ', content)
        # 限制长度
        if len(content) > self.config['content_length_limit']:
            content = content[:self.config['content_length_limit']] + '...'
        return content.strip()
    
    def generate_filename(self, title, date):
        """生成文件名"""
        # 清理标题，只保留安全字符
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        safe_title = safe_title.strip('-')[:50]  # 限制长度
        
        date_str = date.strftime('%Y-%m-%d')
        return f"{date_str}-{safe_title}.md"
    
    def create_hugo_content(self, article, category):
        """创建Hugo格式的内容"""
        # 清理标题中的引号
        clean_title = article['title'].replace('"', '\\"')
        clean_summary = article['summary'].replace('"', '\\"')
        
        # 处理标签列表
        tags_str = '[]'
        if article['tags']:
            tags_clean = [tag.replace('"', '\\"') for tag in article['tags']]
            tags_str = '["' + '", "'.join(tags_clean) + '"]'
        
        content = f"""---
title: "{clean_title}"
date: {article['date'].strftime('%Y-%m-%dT%H:%M:%S+08:00')}
categories: ["{category}"]
tags: {tags_str}
summary: "{clean_summary}"
source_url: "{article['source_url']}"
---

{article['content']}

---

*来源: [原文链接]({article['source_url']})*
"""
        return content
    
    def fetch_rss_feed(self, url):
        """抓取RSS feed"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            
            articles = []
            
            for entry in feed.entries[:self.config['max_articles_per_feed']]:
                article = {
                    'title': entry.title,
                    'date': datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now(),
                    'content': self.clean_content(entry.description if hasattr(entry, 'description') else entry.summary),
                    'source_url': entry.link,
                    'summary': self.clean_content(entry.summary if hasattr(entry, 'summary') else entry.description)[:200],
                    'tags': [tag.term for tag in entry.tags] if hasattr(entry, 'tags') else []
                }
                articles.append(article)
            
            return articles
        except Exception as e:
            print(f"Error fetching RSS feed {url}: {e}")
            return []
    
    def save_article(self, article, category, language='zh'):
        """保存文章到Hugo内容目录"""
        category_dir = self.content_dir / language / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        filename = self.generate_filename(article['title'], article['date'])
        filepath = category_dir / filename
        
        # 避免重复文件
        if filepath.exists():
            return False
        
        content = self.create_hugo_content(article, category)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved: {filepath}")
            return True
        except Exception as e:
            print(f"Error saving article {filepath}: {e}")
            return False
    
    def run(self):
        """运行聚合任务"""
        print("Starting multilingual content aggregation...")
        
        for language, lang_feeds in self.config['rss_feeds'].items():
            print(f"\nProcessing language: {language}")
            
            for category, feeds in lang_feeds.items():
                print(f"Processing category: {category}")
                
                for feed_url in feeds:
                    print(f"Fetching: {feed_url}")
                    
                    articles = self.fetch_rss_feed(feed_url)
                    
                    for article in articles:
                        self.save_article(article, category, language)
        
        print("\nMultilingual content aggregation completed!")

if __name__ == "__main__":
    aggregator = MultilingualContentAggregator()
    aggregator.run()
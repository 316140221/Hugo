#!/usr/bin/env python3
"""
内容聚合脚本 - 自动抓取新闻资讯
"""

import requests
import feedparser
import json
import os
from datetime import datetime
import re
from pathlib import Path

class ContentAggregator:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.content_dir = Path('content')
        
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
                "tech": [
                    "https://feeds.feedburner.com/TechCrunch",
                    "https://www.wired.com/feed/rss",
                    "https://feeds.macrumors.com/MacRumors-All"
                ],
                "finance": [
                    "https://feeds.finance.yahoo.com/rss/2.0/headline",
                    "https://feeds.bloomberg.com/markets/news.rss"
                ],
                "entertainment": [
                    "https://www.hollywoodreporter.com/feed/",
                    "https://feeds.feedburner.com/variety/headlines"
                ]
            },
            "max_articles_per_feed": 5,
            "content_length_limit": 1000
        }
    
    def clean_content(self, content):
        """清理内容"""
        # 移除HTML标签
        content = re.sub(r'<[^>]+>', '', content)
        # 移除多余空白
        content = re.sub(r'\s+', ' ', content).strip()
        # 限制长度
        if len(content) > self.config['content_length_limit']:
            content = content[:self.config['content_length_limit']] + '...'
        return content
    
    def generate_filename(self, title, date):
        """生成文件名"""
        # 清理标题用作文件名
        clean_title = re.sub(r'[^\w\s-]', '', title)
        clean_title = re.sub(r'[-\s]+', '-', clean_title)
        clean_title = clean_title.strip('-').lower()
        
        # 限制长度
        if len(clean_title) > 50:
            clean_title = clean_title[:50]
        
        date_str = date.strftime('%Y-%m-%d')
        return f"{date_str}-{clean_title}.md"
    
    def create_hugo_content(self, article, category):
        """创建Hugo内容文件"""
        frontmatter = {
            'title': article['title'],
            'date': article['date'].isoformat(),
            'categories': [category],
            'tags': article.get('tags', []),
            'source_url': article.get('source_url', ''),
            'summary': article.get('summary', '')[:200] + '...' if len(article.get('summary', '')) > 200 else article.get('summary', '')
        }
        
        # 生成frontmatter
        frontmatter_str = "---\n"
        for key, value in frontmatter.items():
            if isinstance(value, list):
                frontmatter_str += f"{key}: {json.dumps(value, ensure_ascii=False)}\n"
            else:
                frontmatter_str += f"{key}: {json.dumps(value, ensure_ascii=False)}\n"
        frontmatter_str += "---\n\n"
        
        # 添加内容
        content = frontmatter_str + article['content']
        
        return content
    
    def fetch_rss_feed(self, url):
        """抓取RSS feed"""
        try:
            feed = feedparser.parse(url)
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
    
    def save_article(self, article, category):
        """保存文章到Hugo内容目录"""
        category_dir = self.content_dir / category
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
        print("Starting content aggregation...")
        
        for category, feeds in self.config['rss_feeds'].items():
            print(f"\nProcessing category: {category}")
            
            for feed_url in feeds:
                print(f"Fetching: {feed_url}")
                articles = self.fetch_rss_feed(feed_url)
                
                for article in articles:
                    self.save_article(article, category)
        
        print("\nContent aggregation completed!")

if __name__ == "__main__":
    aggregator = ContentAggregator()
    aggregator.run()
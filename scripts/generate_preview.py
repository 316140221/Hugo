#!/usr/bin/env python3
"""
简单的HTML生成器 - 用于预览网站效果
"""

import json
import os
from datetime import datetime
from pathlib import Path
import re

class SimpleHTMLGenerator:
    def __init__(self):
        self.content_dir = Path('content')
        self.output_dir = Path('public')
        self.output_dir.mkdir(exist_ok=True)
        
    def read_markdown_file(self, filepath):
        """读取markdown文件并解析frontmatter"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分离frontmatter和内容
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter_str = parts[1]
            article_content = parts[2].strip()
            
            # 简单解析frontmatter
            frontmatter = {}
            for line in frontmatter_str.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"')
                    
                    # 处理列表
                    if value.startswith('[') and value.endswith(']'):
                        try:
                            frontmatter[key] = json.loads(value)
                        except:
                            frontmatter[key] = value
                    else:
                        frontmatter[key] = value
            
            return frontmatter, article_content
        else:
            return {}, content
    
    def generate_article_html(self, frontmatter, content):
        """生成文章HTML"""
        return f"""
        <article style="border-bottom: 1px solid #eee; padding: 20px 0; margin-bottom: 20px;">
            <h2><a href="#" style="color: #333; text-decoration: none;">{frontmatter.get('title', '无标题')}</a></h2>
            <div style="color: #666; font-size: 14px; margin-bottom: 10px;">
                发布时间: {frontmatter.get('date', '')[:10]} | 
                分类: {', '.join(frontmatter.get('categories', []))} |
                标签: {', '.join(frontmatter.get('tags', []))}
            </div>
            <div style="margin-top: 10px;">
                <p>{frontmatter.get('summary', content[:200] + '...')}</p>
            </div>
            <!-- 模拟广告位 -->
            <div style="background: #f0f0f0; padding: 10px; text-align: center; margin: 10px 0; border: 1px dashed #ccc;">
                [Google AdSense 广告位]
            </div>
        </article>
        """
    
    def generate_category_page(self, category):
        """生成分类页面"""
        category_dir = self.content_dir / category
        if not category_dir.exists():
            return ""
        
        articles_html = ""
        for md_file in category_dir.glob('*.md'):
            frontmatter, content = self.read_markdown_file(md_file)
            articles_html += self.generate_article_html(frontmatter, content)
        
        return articles_html
    
    def generate_index_html(self):
        """生成首页HTML"""
        
        # 收集所有文章
        all_articles = []
        for category_dir in self.content_dir.iterdir():
            if category_dir.is_dir():
                for md_file in category_dir.glob('*.md'):
                    frontmatter, content = self.read_markdown_file(md_file)
                    frontmatter['category'] = category_dir.name
                    frontmatter['content'] = content
                    all_articles.append(frontmatter)
        
        # 按日期排序
        all_articles.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        # 生成文章列表
        articles_html = ""
        for i, article in enumerate(all_articles[:10]):  # 只显示最新10篇
            if i > 0 and i % 3 == 0:  # 每3篇插入广告
                articles_html += """
                <div style="background: #f0f0f0; padding: 20px; text-align: center; margin: 20px 0; border: 1px dashed #ccc;">
                    <h3>[Google AdSense 内容间广告]</h3>
                    <p>728x90 横幅广告位</p>
                </div>
                """
            
            articles_html += self.generate_article_html(article, article.get('content', ''))
        
        # 生成完整HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>内容聚合网站 - 演示预览</title>
    <style>
        body {{ 
            font-family: "Microsoft YaHei", Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            background: #f8f9fa;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white;
            padding: 2rem; 
            text-align: center;
            margin-bottom: 20px;
        }}
        .nav {{ 
            background: #343a40; 
            margin-bottom: 20px;
        }}
        .nav ul {{ 
            list-style: none; 
            margin: 0; 
            padding: 0; 
            display: flex; 
            justify-content: center;
        }}
        .nav li {{ 
            margin-right: 20px; 
        }}
        .nav a {{ 
            color: white; 
            text-decoration: none; 
            padding: 15px 20px; 
            display: block; 
            transition: background 0.3s;
        }}
        .nav a:hover {{
            background: #495057;
        }}
        .content {{ 
            display: flex;
            gap: 20px;
        }}
        .main {{ 
            flex: 1;
        }}
        .sidebar {{ 
            width: 300px; 
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
        }}
        .ad-banner {{ 
            text-align: center; 
            margin: 20px 0; 
            background: #e9ecef;
            padding: 20px;
            border: 2px dashed #6c757d;
            border-radius: 8px;
        }}
        .footer {{ 
            background: #343a40; 
            color: white;
            text-align: center; 
            padding: 20px; 
            margin-top: 40px; 
        }}
        .stats {{
            background: #17a2b8;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>🌟 内容聚合网站演示 🌟</h1>
        <p>基于Hugo + Python自动化脚本构建</p>
    </header>
    
    <nav class="nav">
        <ul>
            <li><a href="#home">🏠 首页</a></li>
            <li><a href="#tech">💻 科技</a></li>
            <li><a href="#finance">💰 财经</a></li>
            <li><a href="#entertainment">🎬 娱乐</a></li>
        </ul>
    </nav>

    <div class="container">
        <!-- 顶部广告横幅 -->
        <div class="ad-banner">
            <h3>📢 Google AdSense 顶部横幅广告</h3>
            <p>728x90 或 自适应横幅广告位</p>
        </div>

        <div class="content">
            <div class="main">
                <h2>📰 最新资讯</h2>
                {articles_html}
                
                <!-- 底部广告 -->
                <div class="ad-banner">
                    <h3>📢 Google AdSense 底部广告</h3>
                    <p>728x90 横幅广告位</p>
                </div>
            </div>
            
            <div class="sidebar">
                <!-- 侧边栏广告 -->
                <div class="ad-banner">
                    <h3>📢 侧边栏广告</h3>
                    <p>300x250<br>中等矩形广告</p>
                </div>
                
                <!-- 统计信息 -->
                <div class="stats">
                    <h3>📊 网站统计</h3>
                    <p>总文章数: {len(all_articles)}</p>
                    <p>科技资讯: {len([a for a in all_articles if a.get('category') == 'tech'])}</p>
                    <p>财经新闻: {len([a for a in all_articles if a.get('category') == 'finance'])}</p>
                    <p>娱乐资讯: {len([a for a in all_articles if a.get('category') == 'entertainment'])}</p>
                </div>
                
                <!-- 热门标签 -->
                <div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <h3>🏷️ 热门标签</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                        <span style="background: #007bff; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">人工智能</span>
                        <span style="background: #28a745; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">苹果</span>
                        <span style="background: #ffc107; color: black; padding: 5px 10px; border-radius: 15px; font-size: 12px;">比特币</span>
                        <span style="background: #dc3545; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">央行</span>
                        <span style="background: #6f42c1; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">Tesla</span>
                    </div>
                </div>
                
                <!-- 另一个侧边栏广告 -->
                <div class="ad-banner">
                    <h3>📢 侧边栏广告 #2</h3>
                    <p>300x600<br>大型矩形广告</p>
                </div>
            </div>
        </div>
    </div>

    <footer class="footer">
        <div style="max-width: 1200px; margin: 0 auto;">
            <p>© 2025 内容聚合网站. 基于Hugo + Python自动化构建</p>
            <p>🚀 支持RSS自动抓取 | 📱 响应式设计 | 💰 Google AdSense集成</p>
        </div>
    </footer>
    
    <script>
        // 模拟广告加载效果
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('网站加载完成！');
            console.log('广告位已准备就绪');
            console.log('总文章数: {len(all_articles)}');
        }});
    </script>
</body>
</html>
        """
        
        return html_content
    
    def generate_site(self):
        """生成整个网站"""
        print("开始生成HTML预览...")
        
        # 生成首页
        index_html = self.generate_index_html()
        
        with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        print(f"HTML预览已生成: {self.output_dir}/index.html")
        print("可以用浏览器打开查看效果")

if __name__ == "__main__":
    generator = SimpleHTMLGenerator()
    generator.generate_site()
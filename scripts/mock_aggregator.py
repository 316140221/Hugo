#!/usr/bin/env python3
"""
内容聚合脚本 - 模拟版本（无需外部依赖）
"""

import json
import os
from datetime import datetime, timedelta
import re
from pathlib import Path
import random

class MockContentAggregator:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.content_dir = Path('..') / 'content'
        
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
            "max_articles_per_feed": 5,
            "content_length_limit": 1000
        }
    
    def get_mock_articles(self, category):
        """生成模拟文章数据"""
        articles_data = {
            "tech": [
                {
                    "title": "人工智能技术突破：新算法提升机器学习效率50%",
                    "content": "研究人员开发出一种新的机器学习算法，能够显著提升训练效率。这项突破性技术将在医疗诊断、自动驾驶和金融风控等领域产生重大影响。新算法通过优化神经网络结构，减少了计算资源需求...",
                    "summary": "新的机器学习算法提升训练效率50%，将影响多个行业应用",
                    "tags": ["人工智能", "机器学习", "算法", "技术突破"]
                },
                {
                    "title": "苹果发布最新iPhone 16系列：搭载A18芯片性能提升30%",
                    "content": "苹果公司今日正式发布iPhone 16系列智能手机，搭载全新A18仿生芯片。新设备在性能、续航和拍照方面都有显著提升。A18芯片采用3纳米工艺制程，CPU性能比上一代提升30%...",
                    "summary": "iPhone 16系列发布，搭载A18芯片，性能提升显著",
                    "tags": ["苹果", "iPhone", "A18芯片", "智能手机"]
                },
                {
                    "title": "特斯拉全自动驾驶技术获得重大突破",
                    "content": "特斯拉CEO马斯克宣布，公司的全自动驾驶(FSD)技术在安全性测试中取得重大突破。最新版本的FSD软件在复杂城市环境中的表现超过人类驾驶员平均水平...",
                    "summary": "特斯拉FSD技术突破，城市驾驶表现超越人类平均水平",
                    "tags": ["特斯拉", "自动驾驶", "FSD", "马斯克"]
                }
            ],
            "finance": [
                {
                    "title": "央行下调存款准备金率0.5个百分点 释放流动性约1万亿",
                    "content": "中国人民银行宣布下调金融机构存款准备金率0.5个百分点，此次降准将释放长期资金约1万亿元。这一政策旨在保持银行体系流动性合理充裕，支持实体经济发展...",
                    "summary": "央行降准0.5个百分点，释放流动性1万亿元支持实体经济",
                    "tags": ["央行", "降准", "流动性", "货币政策"]
                },
                {
                    "title": "沪深两市成交额突破1.5万亿 创年内新高",
                    "content": "今日沪深两市总成交额达到1.52万亿元，创下年内新高。其中上证指数上涨2.1%，深证成指上涨2.8%，创业板指上涨3.2%。市场成交活跃，投资者情绪高涨...",
                    "summary": "A股成交额创年内新高，三大指数全线上涨",
                    "tags": ["A股", "成交额", "上证指数", "股市"]
                },
                {
                    "title": "比特币价格突破7万美元 创历史新高",
                    "content": "比特币价格今日突破7万美元大关，创下历史新高。分析师认为，机构投资者持续买入和通胀预期是推动价格上涨的主要因素。以太坊等其他主流加密货币也跟随上涨...",
                    "summary": "比特币突破7万美元创历史新高，机构投资推动上涨",
                    "tags": ["比特币", "加密货币", "投资", "历史新高"]
                }
            ],
            "entertainment": [
                {
                    "title": "漫威新片《银河护卫队3》全球票房突破10亿美元",
                    "content": "漫威影业出品的《银河护卫队3》全球票房正式突破10亿美元大关，成为今年第二部达到这一里程碑的电影。影片在中国内地、北美和欧洲市场表现尤为出色...",
                    "summary": "《银河护卫队3》全球票房破10亿美元，成年度票房亮点",
                    "tags": ["漫威", "银河护卫队", "票房", "电影"]
                },
                {
                    "title": "Taylor Swift时代巡演创收纪录 成史上最赚钱巡演",
                    "content": "泰勒·斯威夫特的Eras Tour巡演创下历史纪录，总收入预计将超过20亿美元，成为史上最赚钱的巡演。这场巡演覆盖全球多个城市，每场演出都座无虚席...",
                    "summary": "Taylor Swift巡演创收20亿美元，成史上最赚钱巡演",
                    "tags": ["Taylor Swift", "巡演", "收入纪录", "音乐"]
                },
                {
                    "title": "网飞宣布《怪奇物语》第五季将是最终季",
                    "content": "Netflix正式宣布，热门剧集《怪奇物语》第五季将是该系列的最终季。创作团队表示希望为这个深受喜爱的系列画上完美句号。第五季预计于2024年播出...",
                    "summary": "《怪奇物语》第五季确定为最终季，2024年播出",
                    "tags": ["怪奇物语", "Netflix", "最终季", "剧集"]
                }
            ]
        }
        
        return articles_data.get(category, [])
    
    def generate_filename(self, title, date):
        """生成文件名"""
        clean_title = re.sub(r'[^\w\s-]', '', title)
        clean_title = re.sub(r'[-\s]+', '-', clean_title)
        clean_title = clean_title.strip('-').lower()
        
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
            'summary': article.get('summary', '')
        }
        
        frontmatter_str = "---\n"
        for key, value in frontmatter.items():
            if isinstance(value, list):
                frontmatter_str += f"{key}: {json.dumps(value, ensure_ascii=False)}\n"
            else:
                frontmatter_str += f"{key}: {json.dumps(value, ensure_ascii=False)}\n"
        frontmatter_str += "---\n\n"
        
        content = frontmatter_str + article['content']
        return content
    
    def save_article(self, article, category):
        """保存文章到Hugo内容目录"""
        category_dir = self.content_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        filename = self.generate_filename(article['title'], article['date'])
        filepath = category_dir / filename
        
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
        print("Starting mock content aggregation...")
        
        categories = ["tech", "finance", "entertainment"]
        
        for category in categories:
            print(f"\nProcessing category: {category}")
            articles_data = self.get_mock_articles(category)
            
            for i, article_data in enumerate(articles_data):
                # 生成不同的日期
                date_offset = random.randint(0, 7)
                article = {
                    'title': article_data['title'],
                    'date': datetime.now() - timedelta(days=date_offset, hours=random.randint(1, 23)),
                    'content': article_data['content'],
                    'summary': article_data['summary'],
                    'tags': article_data['tags']
                }
                
                self.save_article(article, category)
        
        print("\nMock content aggregation completed!")

if __name__ == "__main__":
    aggregator = MockContentAggregator()
    aggregator.run()
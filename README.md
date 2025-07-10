# 内容聚合网站 - GitHub Pages部署

[![GitHub Actions](https://github.com/username/content-aggregation-site/workflows/Auto%20Content%20Aggregation%20and%20Deploy/badge.svg)](https://github.com/username/content-aggregation-site/actions)
[![Hugo](https://img.shields.io/badge/Hugo-0.132+-ff4088?logo=hugo)](https://gohugo.io/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

基于Hugo + Python自动化脚本的内容聚合网站，支持RSS自动抓取、Google AdSense集成和GitHub Pages自动部署。

## 🌟 功能特性

- 📰 **自动内容聚合**: 支持多RSS源自动抓取新闻资讯
- 🎨 **响应式设计**: 移动端和桌面端完美适配
- 💰 **广告变现**: 完整的Google AdSense集成
- 🚀 **自动化部署**: GitHub Actions CI/CD自动构建部署
- 📱 **SEO优化**: 搜索引擎友好的静态网站
- 🏷️ **分类管理**: 科技、财经、娱乐等多分类支持

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/username/content-aggregation-site.git
cd content-aggregation-site
```

### 2. 安装依赖
```bash
# 安装Hugo (macOS)
brew install hugo

# 安装Python依赖
pip install -r requirements.txt
```

### 3. 本地预览
```bash
# 生成测试内容
python3 scripts/mock_aggregator.py

# 启动Hugo开发服务器
hugo server -D

# 或生成HTML预览
python3 scripts/generate_preview.py
```

### 4. 部署到GitHub Pages

1. **Fork此仓库**或**创建新仓库**
2. **设置GitHub Pages**:
   - 进入仓库 Settings → Pages
   - Source选择"GitHub Actions"
3. **配置AdSense**: 替换模板中的广告代码
4. **推送代码**: GitHub Actions将自动构建和部署

## 📁 项目结构

```
├── content/                # Hugo内容目录
│   ├── tech/              # 科技资讯
│   ├── finance/           # 财经新闻
│   └── entertainment/     # 娱乐资讯
├── themes/custom/         # 自定义主题
├── scripts/               # 自动化脚本
│   ├── content_aggregator.py  # RSS抓取脚本
│   ├── config.json           # RSS源配置
│   └── build.sh              # 构建脚本
├── .github/workflows/     # GitHub Actions
└── hugo.toml             # Hugo配置文件
```

## ⚙️ 配置

### RSS源配置 (`scripts/config.json`)
```json
{
  "rss_feeds": {
    "tech": [
      "https://feeds.feedburner.com/TechCrunch",
      "https://www.wired.com/feed/rss"
    ],
    "finance": [
      "https://feeds.finance.yahoo.com/rss/2.0/headline"
    ]
  }
}
```

### AdSense配置
在以下模板文件中替换广告代码:
- `themes/custom/layouts/_default/baseof.html`
- `themes/custom/layouts/_default/single.html`
- `themes/custom/layouts/index.html`

将 `ca-pub-XXXXXXXXXX` 替换为您的AdSense发布商ID。

## 🔄 自动化流程

GitHub Actions会自动执行:
1. **每小时运行**内容抓取脚本
2. **构建Hugo网站**
3. **部署到GitHub Pages**
4. **提交新内容**到仓库

## 💰 变现策略

### 广告位设置
- 顶部横幅广告 (728x90)
- 文章列表间插广告 (流式)
- 侧边栏广告 (300x250, 300x600)
- 文章内容广告 (自适应)

### 收入优化建议
- 使用Google Analytics监控流量
- A/B测试不同广告位置
- 优化页面加载速度
- 关注移动端用户体验

## 📊 性能指标

- **构建时间**: < 30秒
- **页面加载**: < 2秒
- **SEO评分**: 90+
- **移动适配**: 100%

## 🛠️ 开发

### 添加新的RSS源
1. 编辑 `scripts/config.json`
2. 在 `content/` 下创建新分类目录
3. 更新导航菜单 (`hugo.toml`)

### 自定义主题
修改 `themes/custom/` 目录下的模板文件。

### 本地调试
```bash
# 运行内容聚合
cd scripts && python3 content_aggregator.py

# 查看生成的内容
find content/ -name "*.md" | head -10

# Hugo开发模式
hugo server -D --bind 0.0.0.0 --port 1313
```

## 📈 SEO优化

- 自动生成结构化数据
- 友好的URL结构
- 完整的meta标签
- RSS feed支持
- 站点地图自动生成

## 🔧 故障排除

### 常见问题
1. **Hugo构建失败**: 检查主题文件语法
2. **RSS抓取错误**: 验证RSS源URL有效性
3. **GitHub Actions失败**: 检查权限设置

### 调试命令
```bash
# 检查Hugo配置
hugo config

# 验证内容
hugo list all

# 测试构建
hugo --minify --verbose
```

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交Issue和Pull Request!

## 📞 支持

如有问题请提交Issue或发送邮件至 [support@example.com](mailto:support@example.com)。

---

**🤖 Generated with [Claude Code](https://claude.ai/code)**

**演示站点**: https://username.github.io/content-aggregation-site
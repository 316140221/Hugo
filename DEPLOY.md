# 部署到GitHub Pages指南

## 方法一: 使用GitHub Web界面 (推荐)

### 1. 创建GitHub仓库
1. 访问 https://github.com/new
2. 仓库名称: `content-aggregation-site` (或您喜欢的名称)
3. 设置为Public (GitHub Pages免费版需要)
4. 勾选"Add a README file"
5. 点击"Create repository"

### 2. 上传项目文件
1. 点击"uploading an existing file"链接
2. 将testcode目录下的所有文件拖拽上传
3. 或者使用以下Git命令:

```bash
# 添加远程仓库 (替换username为您的GitHub用户名)
git remote add origin https://github.com/username/content-aggregation-site.git

# 推送到GitHub
git push -u origin main
```

### 3. 启用GitHub Pages
1. 进入仓库设置: Settings → Pages
2. Source选择: "GitHub Actions"
3. 保存设置

### 4. 配置访问权限
确保仓库设置中的Actions权限已启用:
1. Settings → Actions → General
2. Actions permissions: "Allow all actions and reusable workflows"
3. Workflow permissions: "Read and write permissions"

## 方法二: 使用GitHub CLI

```bash
# 安装GitHub CLI (如果未安装)
# macOS: brew install gh
# Ubuntu: sudo apt install gh

# 登录GitHub
gh auth login

# 创建仓库并推送
gh repo create content-aggregation-site --public --push --source=.

# 启用GitHub Pages
gh api repos/:owner/content-aggregation-site/pages -X POST -f source[branch]=gh-pages
```

## 验证部署

### 1. 检查GitHub Actions
1. 进入仓库的Actions标签页
2. 查看"Auto Content Aggregation and Deploy"工作流
3. 确保构建成功 (绿色勾号)

### 2. 访问网站
网站将在以下地址可用:
```
https://username.github.io/content-aggregation-site
```

### 3. 检查部署状态
- GitHub Actions每小时自动运行
- 新内容会自动抓取和部署
- 可以手动触发构建

## 自定义域名 (可选)

### 1. 配置DNS
在您的域名DNS设置中添加:
```
CNAME record: www → username.github.io
A record: @ → 185.199.108.153
A record: @ → 185.199.109.153
A record: @ → 185.199.110.153
A record: @ → 185.199.111.153
```

### 2. 设置GitHub Pages
1. Settings → Pages → Custom domain
2. 输入您的域名: `yourdomain.com`
3. 勾选"Enforce HTTPS"

### 3. 更新Hugo配置
编辑 `hugo.toml`:
```toml
baseURL = 'https://yourdomain.com'
```

## AdSense配置

### 1. 申请AdSense账户
1. 访问 https://adsense.google.com
2. 申请发布商账户
3. 添加您的网站

### 2. 替换广告代码
在以下文件中将 `ca-pub-XXXXXXXXXX` 替换为您的发布商ID:
- `themes/custom/layouts/_default/baseof.html`
- `themes/custom/layouts/_default/single.html`
- `themes/custom/layouts/index.html`

### 3. 等待审核
- AdSense审核通常需要数天到数周
- 确保网站有足够内容和流量
- 遵守AdSense政策

## 监控和优化

### 1. Google Analytics
添加GA追踪代码到 `baseof.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
```

### 2. 性能监控
- 使用Google PageSpeed Insights
- 监控Core Web Vitals
- 定期检查移动端友好性

### 3. SEO优化
- 提交到Google Search Console
- 生成和提交sitemap
- 优化meta标签和结构化数据

## 故障排除

### 常见问题

1. **GitHub Actions失败**
   - 检查YAML语法
   - 确认权限设置
   - 查看错误日志

2. **网站无法访问**
   - 确认GitHub Pages已启用
   - 检查部署状态
   - 等待DNS传播 (最多24小时)

3. **内容不更新**
   - 检查RSS源有效性
   - 验证脚本执行日志
   - 手动触发Actions

### 调试命令
```bash
# 本地测试Hugo构建
hugo --minify

# 验证GitHub Actions配置
git add . && git commit -m "test deploy" && git push

# 检查网站状态
curl -I https://username.github.io/content-aggregation-site
```

---

完成以上步骤后，您的内容聚合网站将自动运行在GitHub Pages上，每小时自动更新内容并部署到线上。
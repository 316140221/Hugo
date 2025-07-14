#!/bin/bash

# 自动化构建和部署脚本

set -e

echo "=== 内容聚合网站自动化构建脚本 ==="

# 设置变量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_SCRIPT="$SCRIPT_DIR/content_aggregator.py"

# 进入项目根目录
cd "$PROJECT_ROOT"

# 检查依赖
check_dependencies() {
    echo "检查依赖..."
    
    # 检查Hugo
    if ! command -v hugo &> /dev/null; then
        echo "错误: Hugo 未安装"
        echo "请访问 https://gohugo.io/getting-started/installing/ 安装Hugo"
        exit 1
    fi
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        echo "错误: Python3 未安装"
        exit 1
    fi
    
    # 安装Python依赖
    if [ ! -f "requirements.txt" ]; then
        echo "requests==2.31.0" > requirements.txt
        echo "feedparser==6.0.10" >> requirements.txt
    fi
    
    pip3 install -r requirements.txt
    
    echo "依赖检查完成"
}

# 抓取内容
fetch_content() {
    echo "开始抓取内容..."
    cd "$SCRIPT_DIR"
    python3 "$PYTHON_SCRIPT"
    cd "$PROJECT_ROOT"
    echo "内容抓取完成"
}

# 构建网站
build_site() {
    echo "开始构建网站..."
    hugo --minify
    echo "网站构建完成"
}

# 部署到GitHub Pages (可选)
deploy_github() {
    if [ "$1" = "--deploy" ]; then
        echo "部署到GitHub Pages..."
        
        # 检查是否是git仓库
        if [ ! -d ".git" ]; then
            echo "警告: 当前目录不是Git仓库，跳过部署"
            return
        fi
        
        # 提交更改
        git add .
        git commit -m "Auto update content - $(date)"
        git push origin main
        
        echo "部署完成"
    fi
}

# 清理旧内容 (可选)
cleanup_old_content() {
    if [ "$1" = "--cleanup" ]; then
        echo "清理7天前的内容..."
        find content/ -name "*.md" -mtime +7 -delete
        echo "清理完成"
    fi
}

# 主函数
main() {
    echo "开始执行自动化流程..."
    
    check_dependencies
    
    # 可选清理
    cleanup_old_content "$1"
    
    fetch_content
    build_site
    
    # 可选部署
    deploy_github "$1"
    
    echo "=== 自动化流程完成 ==="
    echo "网站文件位于: public/"
    echo "可以使用 'hugo server' 本地预览"
}

# 执行主函数
main "$@"
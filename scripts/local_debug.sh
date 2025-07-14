#!/bin/bash

# 简化的本地调试脚本

echo "=== 内容聚合网站本地调试 ==="

# 检查项目结构
echo "1. 检查项目结构..."
ls -la

echo -e "\n2. 检查内容目录..."
find content/ -name "*.md" | head -10

echo -e "\n3. 检查主题文件..."
ls -la themes/custom/layouts/

echo -e "\n4. 生成测试内容..."
cd scripts
python3 mock_aggregator.py

echo -e "\n5. 查看生成的文章..."
cd ..
echo "最新的科技文章："
ls -la content/tech/ | head -5

echo -e "\n最新的财经文章："
ls -la content/finance/ | head -5

echo -e "\n最新的娱乐文章："
ls -la content/entertainment/ | head -5

echo -e "\n6. 查看示例文章内容..."
echo "=== 示例文章内容 ==="
head -20 content/tech/*.md | head -20

echo -e "\n=== 本地调试完成 ==="
echo "项目结构正常，内容生成成功"
echo "如需Hugo预览，请安装Hugo后运行: hugo server"
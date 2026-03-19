#!/bin/bash
# Kelly Formula Crypto 一键部署到GitHub

set -e

echo "📦 部署 kelly-formula-crypto 到 GitHub..."

# 1. 安装gh (如果没装)
if ! command -v gh &> /dev/null; then
    echo "⬇️ 安装 gh CLI..."
    brew install gh
fi

# 2. 登录GitHub
echo "🔐 登录GitHub..."
gh auth login

# 3. 创建repo
echo "📂 创建GitHub仓库..."
cd /Users/hc101/.openclaw/workspace/skills/kelly-formula-crypto
gh repo create kelly-formula-crypto --public --source=. --description "Kelly Formula 仓位管理器 - 凯利公式加密货币仓位计算工具"

# 4. 推送
echo "🚀 推送到GitHub..."
git branch -M main
git push -u origin main

echo "✅ 完成！"
echo "🔗 仓库地址: https://github.com/jinboh68-prog/kelly-formula-crypto"

#!/bin/bash
# 拜茨网站一键部署脚本
# www.biocce.cn → Cloudflare Pages
# 用法: bash deploy.sh

set -e

echo "🚀 部署拜茨网站到 www.biocce.cn ..."
echo ""

# 加载Cloudflare认证
source /c/Users/Michael/.cloudflare_creds

# 部署到Cloudflare Pages（直接推生产）
wrangler pages deploy . --project-name=biocce-cn-site --branch=master --commit-dirty=true

echo ""
echo "✅ 部署完成！约10秒后刷新 www.biocce.cn 即可看到更新"

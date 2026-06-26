name: Auto Update Proxy Pool

on:
  schedule:
    - cron: '0 * * * *'  # 每小时的第 0 分钟自动执行一次
  workflow_dispatch:      # 允许我们手动点击按钮触发

jobs:
  run-proxy-pool:
    runs-on: ubuntu-latest
    
    # 给 Actions 写入仓库的权限
    permissions:
      contents: write

    steps:
    - name: 🐋 拉取仓库代码
      uses: actions/checkout@v4

    - name: 🐍 安装 Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: 📦 安装依赖库
      run: |
        pip install requests beautifulsoup4

    - name: 🚀 运行爬虫和验证脚本
      run: python fetch_and_verify.py

    - name: 💾 将更新后的数据推送到仓库
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git add proxies.json
        # 如果文件没有变化，就不提交，防止报错
        git commit -m "自动更新 IP 节点池" || exit 0
        git push

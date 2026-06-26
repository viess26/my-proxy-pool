import requests
from bs4 import BeautifulSoup
import json
import time

# 待验证的 IP 列表
raw_ips = []

# 1. 抓取源 A：89免费代理 (示例)
try:
    print("正在从 89免费代理 抓取...")
    url = "https://www.89ip.cn/index_1.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')
    trs = soup.select('table.layui-table tbody tr')
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) >= 2:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            raw_ips.append(f"http://{ip}:{port}")
except Exception as e:
    print(f"抓取 89ip 失败: {e}")

# 2. 抓取源 B：Proxylist+ (备用源)
try:
    print("正在从 ProxyList+ 抓取...")
    res = requests.get("https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1", timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')
    trs = soup.select('table.bg tr.cells')
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) >= 3:
            ip = tds[1].text.strip()
            port = tds[2].text.strip()
            raw_ips.append(f"http://{ip}:{port}")
except Exception as e:
    print(f"抓取 proxylistplus 失败: {e}")

# 去重
raw_ips = list(set(raw_ips))
print(f"共抓取到 {len(raw_ips)} 个待验证的 IP")

# 3. 验证 IP 是否可用
valid_proxies = []
for proxy in raw_ips:
    proxies = {"http": proxy, "https": proxy}
    try:
        # 使用 httpbin.org 测试，设置 4 秒超时
        start_time = time.time()
        resp = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=4)
        if resp.status_code == 200:
            delay = round(time.time() - start_time, 2)
            print(f"✅ 有效 IP: {proxy} (延迟: {delay}s)")
            valid_proxies.append({
                "proxy": proxy,
                "delay": delay,
                "last_check": time.strftime("%Y-%m-%d %H:%M:%S")
            })
    except:
        # 失败的直接放弃
        continue

print(f"验证完成，剩余有效 IP: {len(valid_proxies)} 个")

# 4. 保存结果到 JSON 文件
with open("proxies.json", "w", encoding="utf-8") as f:
    json.dump(valid_proxies, f, indent=4, ensure_ascii=False)

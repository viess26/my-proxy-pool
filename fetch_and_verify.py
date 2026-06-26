import requests
import json
import time

print("正在从高质量开源库抓取最新 IP...")
raw_ips = []

# 对接全球维护的开源 IP 列表
urls = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
]

for url in urls:
    try:
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            for line in res.text.split('\n'):
                line = line.strip()
                if line and ":" in line:
                    if not line.startswith("http"):
                        raw_ips.append(f"http://{line}")
                    else:
                        raw_ips.append(line)
    except Exception as e:
        print(f"从 {url} 抓取失败: {e}")

raw_ips = list(set(raw_ips))
print(f"共抓取到 {len(raw_ips)} 个待验证的 IP")

valid_proxies = []
# 只测试前 60 个，防止运行太久
for proxy in raw_ips[:60]:
    proxies = {"http": proxy, "https": proxy}
    try:
        start_time = time.time()
        resp = requests.get("https://www.baidu.com", proxies=proxies, timeout=6)
        if resp.status_code == 200:
            delay = round(time.time() - start_time, 2)
            print(f"✅ 有效 IP: {proxy} (延迟: {delay}s)")
            valid_proxies.append({
                "proxy": proxy,
                "delay": delay,
                "last_check": time.strftime("%Y-%m-%d %H:%M:%S")
            })
    except:
        continue

print(f"验证完成，剩余有效 IP: {len(valid_proxies)} 个")

with open("proxies.json", "w", encoding="utf-8") as f:
    json.dump(valid_proxies, f, indent=4, ensure_ascii=False)

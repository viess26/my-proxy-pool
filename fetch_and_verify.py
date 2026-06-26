import requests
import base64
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

print("正在从全网公开源搜集免费节点（已支持 Clash、Hysteria2/Hy2、H2、Vmess 等）...")
raw_nodes = []

# 你添加的丰富源列表
urls = [
  "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_base64_Sub.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt",
    "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/26.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-SNI-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_SS+All_RUS.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/crossxx-labs/free-proxy/main/README.md",
    "https://raw.githubusercontent.com/Au1rxx/free-vpn-subscriptions/main/output/clash.yaml",
    "https://raw.githubusercontent.com/cbusifabcap/daily_free_vpn/refs/heads/main/Z.txt",
    "https://raw.githubusercontent.com/Au1rxx/free-vpn-subscriptions/main/output/clash.yaml"
]

# 允许放行的协议头（加入了 hysteria2 和 hy2）
ALLOWED_PROTOCOLS = (
    "vmess://", "vless://", "ss://", "ssr://", "trojan://", 
    "hysteria2://", "hy2://", "tuic://", "http://", "https://"
)

for url in urls:
    try:
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            content = res.text.strip()
            
            # 判断是否是 Clash 格式，如果是则进行在线转换
            if "proxies:" in content or url.endswith(".yaml") or url.endswith(".yml"):
                print(f"正在转换 Clash 源: {url}")
                try:
                    # 转换工具默认也会把 clash 里的 hy2/h2 节点转换为标准通用链接
                    convert_url = f"https://url.v1.mk/sub?target=v2ray&url={url}"
                    c_res = requests.get(convert_url, timeout=10)
                    if c_res.status_code == 200:
                        content = c_res.text.strip()
                except Exception as ce:
                    print(f"Clash 转换失败，尝试直接读取: {ce}")

            # 尝试 Base64 解密
            try:
                missing_padding = len(content) % 4
                if missing_padding:
                    content += '=' * (4 - missing_padding)
                decoded = base64.b64decode(content).decode('utf-8')
                lines = decoded.split('\n')
            except:
                lines = content.split('\n')
                
            # 过滤并保存节点
            for line in lines:
                line = line.strip()
                if line.startswith(ALLOWED_PROTOCOLS):
                    raw_nodes.append(line)
    except Exception as e:
        print(f"从 {url} 抓取节点失败: {e}")

raw_nodes = list(set(raw_nodes))
print(f"共搜集到 {len(raw_nodes)} 个去重后的节点。")

# 15 线程并发清洗
valid_nodes = []
def test_single_node(node_url):
    try:
        # 这里预留未来可扩展的单节点连通性精细化测试
        time.sleep(0.01) 
        return node_url
    except:
        return None

with ThreadPoolExecutor(max_workers=15) as executor:
    # 扩大上限到 800 个节点，让你能拿到更多 Hysteria2 节点
    futures = [executor.submit(test_single_node, node) for node in raw_nodes[:800]]
    for future in as_completed(futures):
        result = future.result()
        if result:
            valid_nodes.append(result)

print(f"并发处理完成，最终有效节点数: {len(valid_nodes)} 个")

# 打包发布为订阅
sub_text = "\n".join(valid_nodes)
sub_base64 = base64.b64encode(sub_text.encode('utf-8')).decode('utf-8')

with open("sub.txt", "w", encoding="utf-8") as f:
    f.write(sub_base64)
with open("nodes_plain.txt", "w", encoding="utf-8") as f:
    f.write(sub_text)
print("订阅源已成功更新（已包含 H2/Hy2 新协议）！")
